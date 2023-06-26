import os

import numpy as np
import pandas as pd
import ta
from sqlalchemy import create_engine, text

# Create a connection to your MySQL database
db_connection_str = 'mysql+pymysql://root:'+ os.getenv('DB_PASSWORD') +'@localhost/stock_data'
engine = create_engine(db_connection_str)

query = text("select distinct(symbol) from combined_twenty_year_stocks")
symbol_list = []
with engine.connect() as conn:
    res = conn.execute(query)
    symbol_list = [row[0] for row in res.fetchall()]
    print(symbol_list)

for symbol in symbol_list:
    # Replace with your query to fetch the data
    query = f"SELECT * FROM combined_twenty_year_stocks where symbol = '{symbol}' order by Date asc"

    with engine.connect() as conn:

        # Fetch data from your MySQL table
        df = pd.read_sql(text(query), conn)

        # Calculate indicators
        df['SMA'] = ta.trend.sma_indicator(df['Close'], window=14)
        df['EMA'] = ta.trend.ema_indicator(df['Close'], window=14)
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
        macd_indicator = ta.trend.MACD(df['Close'])
        df['MACD'] = macd_indicator.macd_diff()
        bollinger = ta.volatility.BollingerBands(df['Close'])
        df['Bollinger_High'] = bollinger.bollinger_hband()
        df['Bollinger_Low'] = bollinger.bollinger_lband()
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
        df['Stoch_Oscillator'] = stoch.stoch()
        df['ADX'] = ta.trend.adx(df['High'], df['Low'], df['Close'])
        df['MFI'] = ta.volume.money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'])

        pd.set_option('display.max_columns', None)
        # Write DataFrame to an existing table in your MySQL database
        df = df.replace([np.inf, -np.inf], np.nan)
        df.to_sql('combined_twenty_year_stocks_with_indicators', conn, if_exists='append', index=False)
        conn.commit()
        print(f"inserted {symbol}")
