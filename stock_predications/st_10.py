import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
import os

# --- CONFIGURATION ---
CSV_FILE = 'NSE_1001_TO_1050_start_to_15082020.csv'
OUTPUT_FOLDER = 'top_10_predictions'

# Create a folder to store the 10 CSV files
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def train_xgboost(df):
    df_copy = df.copy()
    # Feature Engineering (Year, Month, Day, etc.)
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

# --- 1. LOAD AND CLEAN DATA ---
all_data = pd.read_csv(CSV_FILE)
all_data.columns = all_data.columns.str.strip().str.upper()
all_data["DATE"] = pd.to_datetime(all_data["DATE"], format="mixed")

# AUTOMATION: Get exactly the FIRST 10 unique symbols from the CSV
first_10_symbols = all_data['SYMBOL'].unique()[:10]
print(f"Symbols to process: {list(first_10_symbols)}\n")

# --- 2. THE LOOP FOR 10 COMPANIES ---
for symbol in first_10_symbols:
    try:
        print(f"Training model for {symbol}...", end=" ")
        
        # Filter and Prepare Data
        df = all_data[all_data['SYMBOL'] == symbol].copy()
        df = df.sort_values("DATE")
        df["target_column"] = df["CLOSE"].astype(float)
        df = df[["DATE", "target_column"]]
        df.set_index("DATE", inplace=True)

        # Train model specifically for this symbol
        model = train_xgboost(df)

        # Generate 30 Business Days (Starting Mon, Aug 17, 2020)
        start_date = "2020-08-17" 
        future_dates = pd.bdate_range(start=start_date, periods=30)
        
        future = pd.DataFrame(index=future_dates)
        future["year"] = future.index.year
        future["month"] = future.index.month
        future["day"] = future.index.day
        future['dayofweek'] = future.index.dayofweek
        future['dayofyear'] = future.index.dayofyear
        future['weekofyear'] = future.index.isocalendar().week.astype(int)

        features = ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'weekofyear']
        predictions = model.predict(future[features])

        # Save each company's prediction to its own CSV
        forecast_df = pd.DataFrame({'Predicted_Close': predictions}, index=future_dates)
        forecast_df.index.name = 'Date'
        file_path = os.path.join(OUTPUT_FOLDER, f"{symbol}_forecast.csv")
        forecast_df.to_csv(file_path)
        
        print(f"✅ Saved to {file_path}")

    except Exception as e:
        print(f"❌ Failed for {symbol}: {e}")

print(f"\nAll 10 predictions are ready in the '{OUTPUT_FOLDER}' folder!")