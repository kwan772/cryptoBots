import os

import yfinance as yf
from sqlalchemy import create_engine
import pandas as pd

def fetch_us_stock_symbols():
    df = pd.read_csv("nasdaq_screener_1686886364917.csv")
    return df['Symbol'].tolist()

# Combine all symbols into one list
all_symbols = fetch_us_stock_symbols()
print(all_symbols)
all_symbols = [symbol for symbol in all_symbols if isinstance(symbol, str) and '^' not in symbol]
print(all_symbols)

db_connection_str = 'mysql+pymysql://root:'+ os.getenv('DB_PASSWORD') +'@localhost/stock_data'
db_connection = create_engine(db_connection_str)

i = all_symbols.index("AOD")
all_symbols = all_symbols[i+1:]
print(all_symbols)

for symbol in all_symbols:
    print(symbol)
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="max")

        hist.index = hist.index.tz_convert(None)  # Convert timezone-aware DateTime to naive DateTime
        hist.reset_index(inplace=True)
        hist.to_sql(f'{symbol}_daily', con=db_connection, if_exists='replace', index=False)
        print(symbol + " saved")
    except Exception as e:
        print(e)
        print(symbol + "skipped")


# ticker = yf.Ticker("AACIW")
# hist = ticker.history(period="max")
# hist.index = hist.index.tz_convert(None) # Convert timezone-aware DateTime to naive DateTime
# hist.reset_index(inplace=True)
# hist.to_sql(f'AA_daily', con=db_connection, if_exists='replace', index=False)
# print(hist)
# print(msft.analyst_price_target)