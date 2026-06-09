## Financial Stock Price Prediction using Forward Validation

A machine learning and time-series forecasting system that predicts stock prices of NSE-listed companies using multiple forecasting approaches. The project compares statistical and machine learning models to generate 30-business-day future stock price forecasts and provides predictions through a lightweight web interface.

## Overview

This project analyzes over 122,000 historical stock market records from 50 NSE-listed companies spanning 2002–2020. It implements and evaluates three forecasting techniques:

XGBoost Regression
ARIMA Time Series Forecasting
Facebook Prophet

The system automatically preprocesses data, trains models, generates future forecasts, and serves predictions through a Flask-based API and web dashboard.

## Key Features
```
1) Multi-model forecasting framework
2) Automated prediction pipeline for 50 stocks
3) 30-business-day forward price prediction
4) Historical data preprocessing and validation
5) Feature engineering for temporal patterns
6) REST API powered by Flask
7) Interactive frontend for stock prediction queries
8) Comparative model evaluation using industry-standard metrics
9) Dataset
10) Source: Yahoo Finance (yfinance)
11) Exchange: National Stock Exchange (NSE), India
12) Companies: 50 NSE-listed stocks
13) Records: 122,000+ daily trading entries
14) Period Covered: July 2002 – August 2020
```
## Features Used
1) Open
2) High
3) Low
4) Close
5) Adjusted Close
6) Volume
7) Date-based engineered features

## Models Implemented
XGBoost

Uses engineered temporal features such as:

Year
Month
Day of Month
Day of Week
Week of Year
Day of Year

Designed to capture non-linear market patterns and calendar-based effects.

## ARIMA

Implements ARIMA(5,1,0) for statistical time-series forecasting and short-term trend prediction.

## Facebook Prophet

Captures long-term trends, seasonality, and structural changes using an additive forecasting framework.

## System Architecture 
```
Data Collection
       ↓
Data Preprocessing
       ↓
Feature Engineering
       ↓
Model Training
       ↓
Forecast Generation
       ↓
CSV Output Storage
       ↓
Flask REST API
       ↓
Web Dashboard
```

## Evaluation Metrics

Model performance is evaluated using:

RMSE (Root Mean Squared Error)
MAE (Mean Absolute Error)
MAPE (Mean Absolute Percentage Error)

## Tech Stack

Backend :-

1) Python
2) Flask

Machine Learning & Forecasting :-

1) XGBoost
2) Statsmodels (ARIMA)
3) Prophet
4) Pandas
5) NumPy
6) Scikit-learn

Frontend :-

1) HTML
2) CSS
3) JavaScript

## Project Structure
```
stock-price-prediction/
│
├── backend/
│   ├── main.py
│   ├── models/
│   └── api/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── datasets/
│
├── predictions/
│   ├── xgboost/
│   ├── arima/
│   └── prophet/
│
├── notebooks/
│
└── README.md
```

## Future Enhancements
1) LSTM-based forecasting models
2) Transformer architectures for financial forecasting
3) Real-time market data integration
4) Cloud deployment
5) Automated model retraining
6) Portfolio recommendation engine
7) Risk-aware forecasting and analytics
