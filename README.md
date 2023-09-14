# Stockaroo - Portfolio Construction and Optimization

Stockaroo is a web-based investment analysis tool that helps you make informed investment decisions based on your income, expenditure, and risk appetite. It provides investment recommendations and allocation strategies tailored to your financial situation and risk tolerance.

## Features

- **Income and Expenditure Analysis:** Enter your income and expenditure details to determine your available investment amount.

- **Risk Appetite Selection:** Choose your risk appetite level (low, medium, or high) to personalize your investment recommendations.

- **Stock Screening:** Stockaroo screens and suggests potential stocks based on your risk appetite and available investment amount.

- **Portfolio Optimization:** It optimizes your portfolio allocation to maximize returns based on your financial situation and risk tolerance.

- **Investment Allocation:** Get recommendations on how to allocate your available investment amount, including suggestions for fixed deposits.

- **Interactive Pie Chart:** Visualize your investment allocation with an interactive pie chart, showing stock names and amounts.

## Deployment

This project has been deployed using Azure App Service for hosting the web application and Azure Container Registry for containerized deployment.

### Azure App Service

The Stockaroo web application is hosted on Azure App Service, a fully managed platform for building, deploying, and scaling web apps. Azure App Service offers high availability, automatic scaling, and easy integration with Azure services.

### Azure Container Registry

Azure Container Registry is used to store and manage Docker container images for the Stockaroo application. Docker containers make it easy to package the application and its dependencies, ensuring consistency and portability across different environments.

## Getting Started

To get started with Stockaroo, follow these steps:

1. Clone the repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.
4. Access the web interface by opening a web browser and navigating to `http://localhost:5000`.

## Usage

1. Select your risk appetite (low, medium, or high).
2. Enter your income and expenditure details.
3. Stockaroo will provide you with investment recommendations and allocation strategies.
4. Explore the interactive pie chart to visualize your investment allocation.

## Technologies Used

- Python
- Flask
- HTML/CSS
- BeautifulSoup
- Matplotlib
- yfinance
- NumPy
- pandas
- pypfopt

## Screenshots

![Screenshot 1](/screenshots/stockaroo1.png)
![Screenshot 2](/screenshots/stockaroo0.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
