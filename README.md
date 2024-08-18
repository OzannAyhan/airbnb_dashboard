# Airbnb Price Prediction and Forecasting Application

## Summary
This Python application is designed to analyze and forecast Airbnb prices across different locations in various cities. By using historical Airbnb data, the application predicts price changes based on location, providing valuable insights for hosts and travelers alike. The application is Dockerized for ease of deployment and has been deployed on Heroku for accessibility.

## Features
- *Data Analysis*: Analyzes Airbnb price trends based on location.
- *Forecasting*: Predicts future prices using advanced machine learning models.
- *Interactive Visualizations*: Provides visual insights into pricing trends.

## Technology Stack
- *Python*: The core programming language used for data processing, analysis, and forecasting.
- *Docker*: Containerizes the application for easy deployment across different environments.
- *Heroku*: The platform used for deploying the application to the cloud.
- *Flask*: The web framework used to build the web interface.
- *Pandas*: Used for data manipulation and analysis.
- *Prophet (or any other forecasting model)*: Used for price prediction and forecasting.

## How to Run Locally

### Prerequisites
- *Docker*: Ensure Docker is installed on your machine.
- *Python 3.x*: Required if you want to run the application without Docker.

### Step 1: Clone the Repository
Clone the GitHub repository to your local machine:

bash
git clone https://github.com/yourusername/airbnb-price-forecasting.git
cd airbnb-price-forecasting


### Step 2: Build the Docker Image
Navigate to the project directory and build the Docker image:

bash
docker build -t airbnb-price-app .


### Step 3: Run the Application in Docker
After building the image, run the Docker container:

bash
docker run -p 5000:5000 airbnb-price-app


The application will be accessible at http://localhost:5000 in your web browser.

### Step 4 (Alternative): Run the Application Locally without Docker

1. *Install Dependencies*:
    bash
    pip install -r requirements.txt
    

2. *Run the Application*:
    bash
    python app.py
    

The application will be accessible at http://localhost:5000 in your web browser.

## Deployed Application on Heroku

The application has been deployed on Heroku and can be accessed at the following link:

[https://airbnb-dashboard.herokuapp.com](https://airbnb-dashboard.herokuapp.com)
