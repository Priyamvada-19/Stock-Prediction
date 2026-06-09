import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
import os

# --- CONFIGURATION ---
CSV_FILE = 'NSE_1001_TO_1050_start_to_15082020.csv'
OUTPUT_FOLDER = 'stock_predictions_output'

# Create an output folder so your desktop doesn't get cluttered
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def train_xgboost(df):
    df_copy = df.copy()
    # Feature Engineering
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

# Get a list of every unique symbol in the file
all_symbols = all_data['SYMBOL'].unique()
print(f"Found {len(all_symbols)} unique companies. Starting batch prediction...\n")

# --- 2. THE AUTOMATION LOOP ---
for current_symbol in all_symbols:
    try:
        print(f"Processing: {current_symbol}...", end=" ")
        
        # Filter for this specific symbol
        df = all_data[all_data['SYMBOL'] == current_symbol].copy()
        
        if len(df) < 10: # Skip companies with too little data
            print("Skipped (Not enough data)")
            continue
            
        df = df.sort_values("DATE")
        df["target_column"] = df["CLOSE"].astype(float)
        df = df[["DATE", "target_column"]]
        df.set_index("DATE", inplace=True)

        # Train model
        model = train_xgboost(df)

        # Generate 30 Business Days forecast (Starting Aug 17, 2020)
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

        # Save to CSV in the output folder
        forecast_df = pd.DataFrame({'Predicted_Close': predictions}, index=future_dates)
        forecast_df.index.name = 'Date'
        file_path = os.path.join(OUTPUT_FOLDER, f"{current_symbol}_forecast.csv")
        forecast_df.to_csv(file_path)
        
        print(f"Done! Saved to {file_path}")

    except Exception as e:
        print(f"Failed! Error: {e}")

print("\n✅ All predictions complete! Check the 'stock_predictions_output' folder.")