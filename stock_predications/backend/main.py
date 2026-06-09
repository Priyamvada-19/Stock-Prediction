import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Stock Prediction API")

# Allow CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "stock_predictions.csv")
TOP_10_DIR = os.path.join(BASE_DIR, "stock_predictions_output")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Serve frontend static files
app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

class NextDayPrediction(BaseModel):
    company: str
    last_date: str
    prediction_date: str
    current_price: float
    predicted_next_day_price: float
    direction: str
    change_percent: float

class ForecastData(BaseModel):
    date: str
    predicted_close: float

class FullPredictionResponse(BaseModel):
    next_day: NextDayPrediction
    forecast_30_days: Optional[List[ForecastData]] = None

@app.get("/api/companies", response_model=List[str])
def get_companies():
    """Returns a list of all company tickers available."""
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=500, detail="Prediction data file not found.")
    
    df = pd.read_csv(CSV_PATH)
    companies = df["Company"].dropna().unique().tolist()
    return sorted(companies)

@app.get("/api/prediction/{company_ticker}", response_model=FullPredictionResponse)
def get_prediction(company_ticker: str):
    """Returns next day prediction and 30-day forecast if available."""
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=500, detail="Prediction data not found.")
    
    df = pd.read_csv(CSV_PATH)
    company_row = df[df["Company"] == company_ticker]
    
    if company_row.empty:
        raise HTTPException(status_code=404, detail="Company not found in predictions.")
    
    row = company_row.iloc[0]
    next_day = NextDayPrediction(
        company=row["Company"],
        last_date=row["Last Data Date"],
        prediction_date=row["Prediction Date"],
        current_price=row["Current Price (₹)"],
        predicted_next_day_price=row["Predicted Next Day Price (₹)"],
        direction=row["Direction"],
        change_percent=row["Change %"]
    )
    
    forecast_30_days = None
    forecast_file = os.path.join(TOP_10_DIR, f"{company_ticker}_forecast.csv")
    
    if os.path.exists(forecast_file):
        forecast_df = pd.read_csv(forecast_file)
        forecast_30_days = [
            ForecastData(date=str(f_row["Date"]), predicted_close=float(f_row["Predicted_Close"]))
            for _, f_row in forecast_df.iterrows()
        ]
        
    return FullPredictionResponse(next_day=next_day, forecast_30_days=forecast_30_days)
