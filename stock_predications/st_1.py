import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor

# --- CONFIGURATION ---
TARGET_SYMBOL = "SPIC.NS"  # Change this to the symbol you want to predict
CSV_FILE = 'NSE_1001_TO_1050_start_to_15082020.csv'

def train_xgboost(df):
    df_copy = df.copy()
    # Feature Engineering (Extracting time data for XGBoost)
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.month
    df_copy['day'] = df_copy.index.day
    df_copy['dayofweek'] = df_copy.index.dayofweek
    df_copy['dayofyear'] = df_copy.index.dayofyear
    df_copy['weekofyear'] = df_copy.index.isocalendar().week.astype(int)

    features = ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'weekofyear']
    X = df_copy[features]
    y = df_copy['target_column'] 

    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, tree_method='hist')
    model.fit(X, y)
    return model

# --- 1. DATA LOADING & HEADER CLEANING ---
all_data = pd.read_csv(CSV_FILE)

# IMPORTANT: This line cleans your column names (removes spaces, fixes capitalization)
all_data.columns = all_data.columns.str.strip().str.upper()

print("Columns found in CSV:", all_data.columns.tolist())

# Convert Date to datetime format
all_data["DATE"] = pd.to_datetime(all_data["DATE"], format="mixed")

# --- 2. FILTERING BY SYMBOL ---
# We check the 'SYMBOL' column for your specific company
df = all_data[all_data['SYMBOL'] == TARGET_SYMBOL.upper()].copy()

if df.empty:
    available = all_data['SYMBOL'].unique()[:5]
    print(f"\n❌ Error: '{TARGET_SYMBOL}' not found. Available examples: {available}")
else:
    # Sort by date and set as index
    df = df.sort_values("DATE")
    df["target_column"] = df["CLOSE"].astype(float)
    df = df[["DATE", "target_column"]]
    df.set_index("DATE", inplace=True)

    # --- 3. MODEL TRAINING ---
    model = train_xgboost(df)
    print(f"\n✅ Model trained successfully for symbol: {TARGET_SYMBOL}")

    # --- 4. GENERATE BUSINESS DAYS (Excluding Weekends) ---
    # Starts from Monday, Aug 17, 2020 as requested
    start_pred_date = "2020-08-17" 
    future_dates = pd.bdate_range(start=start_pred_date, periods=30)

    future = pd.DataFrame(index=future_dates)
    future["year"] = future.index.year
    future["month"] = future.index.month
    future["day"] = future.index.day
    future['dayofweek'] = future.index.dayofweek
    future['dayofyear'] = future.index.dayofyear
    future['weekofyear'] = future.index.isocalendar().week.astype(int)

    features = ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'weekofyear']
    predictions = model.predict(future[features])

    # --- 5. SAVE TO CSV ---
    forecast_df = pd.DataFrame({'Predicted_Close': predictions}, index=future_dates)
    forecast_df.index.name = 'Date'
    file_name= f"{TARGET_SYMBOL}_30day_forecast.csv"
    forecast_df.to_csv(file_name)
    print(f"📊 Predictions saved to: {file_name}")

    # --- 6. VISUALIZATION ---
    plt.figure(figsize=(12,6))
    # Show history (last 50 days) and 30-day forecast
    plt.plot(df.index[-50:], df["target_column"][-50:], label="Actual History", color='#1f77b4', linewidth=2)
    plt.plot(future_dates, predictions, label="XGBoost Forecast (M-F)", color='#ff7f0e', linestyle='--', marker='o')
    
    plt.title(f"30-Day Stock Price Prediction: {TARGET_SYMBOL}", fontsize=14, fontweight='bold')
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=30)
    plt.tight_layout()
    
    print("Opening Graph... (Close window to exit)")
    plt.show()