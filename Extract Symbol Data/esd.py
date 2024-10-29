import yfinance as yf
import pandas as pd
from google.colab import files
import datetime

# Function to extract OHLC data for a given symbol
def extract_symbol_data(symbol, period, interval):
    # Check if the interval is valid
    if interval not in ['1d', '1h']:
        raise ValueError("Invalid interval! Use '1d' for daily or '1h' for hourly.")
    
    # Download the OHLC data
    data = yf.download(tickers=symbol, period=period, interval=interval)
    
    # Prepare the file name
    file_name = f'esd_{symbol.replace("/", "")}_{period}_{interval}.csv'
    
    # Save the data to a CSV file
    data.to_csv(file_name)
    
    return file_name

# Function to adjust datetime values with '+01:00' timezone
def adjust_datetime(file_name):
    # Load the CSV file into a DataFrame, skipping any extraneous rows
    data = pd.read_csv(file_name, skiprows=0)  # Adjust if there are extra headers
    
    # Verify and ensure the first column is 'Datetime' and convert it to datetime format
    data.iloc[:, 0] = pd.to_datetime(data.iloc[:, 0], errors='coerce')
    
    # Drop rows with NaT in the datetime column, which indicates parsing issues
    data = data.dropna(subset=[data.columns[0]])
    
    # Iterate over the rows and adjust datetime
    for index, row in data.iterrows():
        if row[0].strftime('%z') == '+0100':  # Check for +01:00 timezone
            # Subtract 1 hour
            adjusted_time = row[0] - datetime.timedelta(hours=1)
            
            # Update the row's Datetime value
            data.at[index, data.columns[0]] = adjusted_time
    
    # Save the adjusted DataFrame back to the CSV
    adjusted_file_name = file_name
    data.to_csv(adjusted_file_name, index=False)
    
    # Download the adjusted CSV
    files.download(adjusted_file_name)

# Main function to extract symbol data and adjust datetime
def main(symbol, period, interval):
    # Step 1: Extract symbol data and save it to a CSV
    file_name = extract_symbol_data(symbol, period, interval)
    
    # Step 2: Adjust datetime values in the CSV if needed
    adjust_datetime(file_name)

# Example usage
symbol = 'BTC-USD'  # Replace with your desired symbol
period = '2y'        # Replace with your desired period
interval = '1d'      # Use '1d' for daily or '1h' for hourly

main(symbol, period, interval)
