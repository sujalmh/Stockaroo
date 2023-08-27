import io

import base64
from bs4 import BeautifulSoup
import requests
import matplotlib
import matplotlib.pyplot as plt

import yfinance as yf
import numpy as np
import pandas as pd
from pypfopt import risk_models
from pypfopt import plotting
from pypfopt import expected_returns
from pypfopt import EfficientFrontier
from pypfopt import DiscreteAllocation

matplotlib.use("Agg")


from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

investor_choice = ""

@app.route("/", methods=["GET", "POST"])
def select_investor():
    global investor_choice
    
    if request.method == "POST":
        investor_choice = request.form.get("investor_choice")
        return redirect(url_for("add_info"))
    
    return render_template("select_investor.html")

@app.route("/add_info", methods=["GET", "POST"])
def add_info():
    global investor_choice, result, plot_image

    
    if investor_choice == "":
        return redirect(url_for("select_investor"))
    
    # Declare result and plot_image locally within the function
    result = None
    plot_image = None
    available_investment = 0
    fixed_deposit = 0
    table_data=[]
    top_5_stocks = []  
    result = dict()
    if request.method == "POST":
        income = float(request.form.get("income"))
        expenditure = float(request.form.get("expenditure"))
        risk_appetite = request.form.get("risk_appetite")
        savings=income-expenditure
        savings_percent = (savings / income) * 100

        if risk_appetite=="low":
            link = f'https://www.screener.in/screens/1150160/large_cap/'

        elif risk_appetite=="mid":
            link = f'https://www.screener.in/screens/1151198/mid_cap/'

        else:
            link = f'https://www.screener.in/screens/973/small-cap-high-roce/'

        if savings_percent < 25:
            risk_suggestion = "low"
            available_investment = savings * 0.75
            fixed_deposit = savings - available_investment

        elif 25 <= savings_percent <= 35:
            risk_suggestion = "medium"
            available_investment = savings * 0.65
            fixed_deposit = savings - available_investment
      
        else:
            risk_suggestion = "high"
            available_investment = savings * 0.25
            fixed_deposit = savings - available_investment

        table_data = [
            ("Available Investment Amount", f"₹ {available_investment:.2f}"),
            ("Amount for Fixed Deposit", f"₹ {fixed_deposit:.2f}")
        ]



        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }


        req = requests.get(link, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        i = 0
        table_html = soup.find("tbody")
        for tr in soup.find_all("tr"):

            if i != 0:
                td_html = tr.find_all('td')
                try:
                    a_html = td_html[1].find('a', href=True)
                    href = a_html['href']
                    ticker = ""
                    c = 9
                    print(href)
                    while (href[c] != "/"):
                        ticker += href[c]
                        c += 1
                    result[ticker] = a_html.getText().strip()
                except:
                    continue

            i += 1
        stock_list=""
        stock_name=list(result.values())
        stocks = result.keys()
        for sname in stocks:
            stock_list+=(sname+" ")
        stock_list.split()
        tickers = stock_list.split()

        for count in range(len(tickers)):
            try:
                int(tickers)
                tickers[count] = "^" + tickers[count]
            except:
                tickers[count] = tickers[count] + ".NS"

        ohlc = yf.download(tickers, period="max")
        ohlc=ohlc.dropna(axis=1, how='all')

        prices = ohlc["Adj Close"].dropna(how="all")

        prices.replace(np.nan, 0)
        sample_cov = risk_models.sample_cov(prices, frequency=252)
        S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
        mu = expected_returns.capm_return(prices)
        S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()

        ef = EfficientFrontier(None, S, weight_bounds=(None, None))
        ef.min_volatility()
        weights = ef.clean_weights()
        pd.Series(weights).plot.barh()
        ef.portfolio_performance(verbose=True)
        latest_prices = prices.iloc[-1]

        da = DiscreteAllocation(weights, latest_prices,
                                total_portfolio_value=savings, short_ratio=0.3)
        alloc, leftover = da.greedy_portfolio()
       
        mu = expected_returns.capm_return(prices)
        S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()

        ef = EfficientFrontier(mu, S)


        ef.max_sharpe()
        weights = ef.clean_weights()
        ratio = weights.values()
        number = []
        amount = []
        ratio = list(ratio)

        for n in range(len(latest_prices)):
            amount.append(savings*ratio[n])
            number.append(amount[n]/latest_prices[n])


            result = {
        "Income": income,
        "Expenditure": expenditure,
        "Risk Appetite": risk_appetite,
        "Savings Percent": f"{savings_percent:.2f}%",
        "Suggested Risk": risk_suggestion,
        "Leftover": leftover
    }
    
        
        plot_image = generate_plot(ratio, weights.keys())
        if request.method == "GET":
            result = None
            plot_image = None
        
        top_5_stocks = [(str(ticker)[:-3], stock_name[tickers.index(ticker)], number,np.float64(number)*latest_prices[ticker]) for ticker, (ticker,number) in zip(tickers, alloc.items())][:5]


    return render_template("add_info.html", result=result, plot_image=plot_image, top_5_stocks=top_5_stocks, table_data=table_data)

def generate_plot(ratio, name):   
   
    plt.title('Income vs Expenditure')
    sorted_indices = sorted(range(len(name)), key=lambda k: ratio[k], reverse=True)
    top_5_indices = sorted_indices[:5]

    explode = [0.1 if i in top_5_indices else 0 for i in range(len(name))]
    plt.figure(figsize=(8,8))

    plt.pie(ratio, labels=name,autopct='%1.2f%%',startangle=140)
    patches, texts = plt.pie(ratio, startangle=140)
    plt.legend(patches, name, loc="best")
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return img_base64

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

