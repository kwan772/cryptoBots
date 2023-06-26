import os

from sqlalchemy import create_engine, text
import pandas as pd

db_connection_str = 'mysql+pymysql://root:'+ os.getenv('DB_PASSWORD') +'@localhost/stock_data'
engine = create_engine(db_connection_str)

with engine.connect() as conn:
    query = text(f"""
        select * from twenty_year_stocks
    """)
    result = conn.execute(query)
    rows = result.fetchall()
    all_symbols = [row[0] for row in rows]
    print(all_symbols)

# And it has the same schema as your individual stock tables, plus a 'symbol' column
for symbol in all_symbols:
    table_name = f"{symbol}_daily"
    # select rows between the date range and insert into the new table
    query = text(f"""
            INSERT INTO combined_twenty_year_stocks (Date, Open, High, Low, Close, Volume, Dividends, `Stock Splits`, Symbol)
            SELECT Date, Open, High, Low, Close, Volume, Dividends, `Stock Splits`, '{symbol}' as Symbol FROM {table_name}
            WHERE Date BETWEEN '2000-01-01' AND '2023-06-15'
        """)
    try:
        with engine.connect() as connection:
            connection.execute(query)
            connection.commit()  # Committing the transaction
    except Exception as e:
        print(f"Error occurred for {table_name}: {e}")
