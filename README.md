# EasyStocks
**EasyStocks** is a simple stock portfolio web-service which helps to track related news, dividends and price movements. Popular USA and Russian stocks are available.

![](/static/img/about/main.png)
![](/static/img/about/stocks_us.png)

---

## Technologies
* [Django](https://docs.djangoproject.com/en/3.1/)
* [Alpha Vantage API](https://www.alphavantage.co/) for getting a financial data
* [Plotly](https://plot.ly/) for data visualization
* [Chart.js](https://www.chartjs.org/) for data visualization
* [Celery](http://docs.celeryproject.org/en/latest/#) for task scheduling
* [NewsAPI](https://newsapi.org/) for news

## Running EasyStocks with Docker

To run EasyStocks using Docker, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/iabramov/EasyStocks.git
    cd EasyStocks
    ```

2. **Build the Docker image:**
    ```sh
    docker build -t easystocks .
    ```

3. **Run the Docker container:**
    ```sh
    docker run -d -p 8000:8000 easystocks
    ```

4. **Access the application:**
    Open your web browser and go to `http://localhost:8000`.

Make sure you have Docker installed on your machine before running these commands.
