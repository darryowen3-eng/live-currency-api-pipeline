import pandas as pd
import requests

# Pull Live Data
print("Connecting to live web financial registry...")

api_url = "https://open.er-api.com/v6/latest/USD"

# Standard browser agent headers to ensure smooth connection
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    # Fetch live data safely using requests
    response = requests.get(api_url, headers=headers)
    
    # Checking if the connection was successful
    if response.status_code == 200:
        web_data = response.json()
        print("Live data successfully extracted from the web!")
        
        # Isolate exchange rates relative to USD
        rates_dict = web_data['rates']
        
        # Convert dictionary into a structured DataFrame
        raw_df = pd.DataFrame(list(rates_dict.items()), columns=['Currency_Code', 'Exchange_Rate'])
    else:
        print(f"Server responded with error status: {response.status_code}")
        exit()
        
except Exception as e:
    print(f"Connection error occurred: {e}")
    exit()

# PHASE 2: TRANSFORM (Clean and Filter for ZMW
print("Transforming web metrics...")

# 1. Add tracking metadata (The exact timestamp of data retrieval)
raw_df['Extraction_Date'] = pd.to_datetime(web_data['time_last_update_utc']).date()

# 2. Filter records to target Zambia (ZMW) and main regional partners
target_currencies = ['ZMW', 'ZAR', 'CNY', 'GBP']
clean_df = raw_df[raw_df['Currency_Code'].isin(target_currencies)].copy()

# Reset index to look clean
clean_df = clean_df.reset_index(drop=True)

print("\n--- CLEANED LIVE EXCHANGE METRICS ---")
print(clean_df)



import sqlalchemy

# ==========================================
# Streaming Live Tables to MySQL
print("\nConnecting to analytical storage...")

db_username = 'root'
db_password = 'darry@2005'  
db_name = 'retail_analytics'

try:
    connection_url = sqlalchemy.engine.URL.create(
        drivername="mysql+mysqlconnector",
        username=db_username,
        password=db_password,
        host="127.0.0.1",
        port=3306,
        database=db_name
    )
    
    # Creating the connection engine
    engine = sqlalchemy.create_engine(connection_url)
    
    # 3. Streaming data straight to my database
    print("Uploading live currency indexes...")
    # We use if_exists='replace' so it always holds the freshest daily currency value
    clean_df.to_sql('dim_currency_rates', con=engine, if_exists='replace', index=False)
    
    print("Success! Live web exchange metrics have populated your MySQL database.")

except Exception as e:
    print(f"\Database Connection Error: {e}")

