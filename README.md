## Financial Stock Price Prediction using Forward Validation

A machine learning and time-series forecasting system that predicts stock prices of NSE-listed companies using multiple forecasting approaches. The project compares statistical and machine learning models to generate 30-business-day future stock price forecasts and provides predictions through a lightweight web interface.

## Overview

This project analyzes over 122,000 historical stock market records from 50 NSE-listed companies spanning 2002–2020. It implements and evaluates three forecasting techniques:

XGBoost Regression
ARIMA Time Series Forecasting
Facebook Prophet

The system automatically preprocesses data, trains models, generates future forecasts, and serves predictions through a Flask-based API and web dashboard.

## Key Features
Multi-model forecasting framework
Automated prediction pipeline for 50 stocks
30-business-day forward price prediction
Historical data preprocessing and validation
Feature engineering for temporal patterns
REST API powered by Flask
Interactive frontend for stock prediction queries
Comparative model evaluation using industry-standard metrics
Dataset
Source: Yahoo Finance (yfinance)
Exchange: National Stock Exchange (NSE), India
Companies: 50 NSE-listed stocks
Records: 122,000+ daily trading entries
Period Covered: July 2002 – August 2020

## Features Used
Open
High
Low
Close
Adjusted Close
Volume
Date-based engineered features

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

Python
Flask

Machine Learning & Forecasting :-

XGBoost
Statsmodels (ARIMA)
Prophet
Pandas
NumPy
Scikit-learn

Frontend :-

HTML
CSS
JavaScript

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
LSTM-based forecasting models
Transformer architectures for financial forecasting
Real-time market data integration
Cloud deployment
Automated model retraining
Portfolio recommendation engine
Risk-aware forecasting and analytics
