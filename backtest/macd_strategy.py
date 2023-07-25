import os
from sqlalchemy import create_engine, text
import ta
import pandas as pd

db_connection_str = 'mysql+pymysql://root:'+ os.getenv('DB_PASSWORD') +'@localhost/stock_data'
engine = create_engine(db_connection_str)
df = None
with engine.connect() as conn:
    query = text("select * from new_stock_price where symbol = 'amzn' order by date asc")
    conn.execute(query)
    df = pd.read_sql(query, conn)

    conn.commit()

    print(df)

df["macd"] = ta.trend.macd(df['Close'], window_slow=26, window_fast=12, fillna=False)
pd.set_option('display.max_columns', None)
print(df)

