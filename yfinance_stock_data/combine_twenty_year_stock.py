import os
from datetime import datetime

from sqlalchemy import create_engine,text
import pandas as pd

def fetch_us_stock_symbols():
    df = pd.read_csv("nasdaq_screener_1686886364917.csv")
    return df['Symbol'].tolist()

def convert_to_table(data):
    # Assuming 'engine' is the SQLAlchemy engine you've created

    # Convert list to DataFrame
    df = pd.DataFrame(data, columns=['Symbol'])

    # Save DataFrame to new MySQL table
    df.to_sql('twenty_year_stocks', con=engine, index=False, if_exists='replace')

# Combine all symbols into one list
all_symbols = fetch_us_stock_symbols()
# print(all_symbols)
all_symbols = [symbol for symbol in all_symbols if isinstance(symbol, str) and '^' not in symbol]
# print(all_symbols)

db_connection_str = 'mysql+pymysql://root:'+ os.getenv('DB_PASSWORD') +'@localhost/stock_data'
engine = create_engine(db_connection_str)

twenty_year_list = []

for table in all_symbols:
    with engine.connect() as conn:

        try:
            # Query the minimum date from the table
            query = text(f"SELECT MIN(Date) FROM {table}_daily")
            result = conn.execute(query)
            min_date = result.scalar()  # Fetch the first column of the first row

            # If the minimum date is later than 2000-01-01
            if min_date is not None and min_date < datetime(2000, 1, 1):
                twenty_year_list.append(table)
        except Exception:
            continue

print(twenty_year_list)
convert_to_table(twenty_year_list)





