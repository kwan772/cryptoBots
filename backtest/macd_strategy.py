import os
from datetime import datetime

from sqlalchemy import create_engine, text
import ta
import pandas as pd
import queue

db_connection_str = 'mysql+pymysql://root:'+ os.getenv('DB_PASSWORD') +'@localhost/stock_data'
engine = create_engine(db_connection_str)
df = None
with engine.connect() as conn:
    query = text("select * from new_stock_price where symbol = 'wmt' order by date asc")
    conn.execute(query)
    df = pd.read_sql(query, conn)

    conn.commit()

    # print(df)

df["macd"] = ta.trend.macd(df['Close'], window_slow=26, window_fast=12, fillna=False)
df["macd_diff"] = ta.trend.macd_diff(df['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=False)
df["mac_signal"] = ta.trend.macd_signal(df['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=False)
df["ema"] = ta.trend.ema_indicator(df['Close'], window=200, fillna=False)
df = df[(df['Date'] >= '2015-12-01') & (df['Date'] <= '2023-05-01')]
df = df.dropna()
pd.set_option('display.max_columns', None)
# print(df)


macd_queue = queue.Queue()
previous_macd_diff = None
macd_sum = 0
is_invested = False
is_market_buy_order = False
is_market_sell_order = False
cash = 100000
shares = 0
orders = 0
entry_price = None
entry_date = None
wins = 0
losses = 0
total_win_percentage = 0
total_loss_percentage = 0
total_trade_days = 0

def is_macd_cross(current_macd_diff):
    global previous_macd_diff
    if previous_macd_diff >= 0 and current_macd_diff < 0:
        return True
    if previous_macd_diff <= 0 and current_macd_diff > 0:
        return True
    if current_macd_diff == 0:
        return True

    return False

def process_macd_queue(macd):
    global macd_queue, macd_sum
    days = 100
    queue_len = macd_queue.qsize()
    current_macd = abs(macd)

    if queue_len >= days:
        macd_sum -= macd_queue.get()

    macd_sum += current_macd
    macd_queue.put(current_macd)

def process_orders(row):
    global cash, shares, is_market_sell_order, is_market_buy_order, entry_date, is_invested, total_trade_days, orders, entry_price, wins, losses, total_win_percentage, total_loss_percentage
    if is_market_sell_order:
        cash += shares * row['Open']
        shares = 0
        is_market_sell_order = False
        is_invested = False
        orders += 1
        exit_price = row['Open']
        if exit_price > entry_price:
            wins+=1
            total_win_percentage += (exit_price / entry_price -1) * 100
        else:
            losses += 1
            total_loss_percentage += (exit_price / entry_price -1) * 100
        entry_price = None
        # total_trade_days += (entry_date - datetime.strptime(row['Date'], '%Y-%m-%d')).days
        total_trade_days += (row['Date'] - entry_date).days
        entry_date = None

    if is_market_buy_order:
        shares += float(cash / row['Open'])
        cash = 0
        is_market_buy_order = False
        is_invested = True
        orders += 1
        entry_price = row['Open']
        entry_date = row['Date']
        # entry_date = datetime.strptime(row['Date'], '%Y-%m-%d')

# df should be defined here. For example:
# df = pd.read_csv('your_data.csv')

for index, row in df.iterrows():
    process_orders(row)
    current_macd_diff = row["macd_diff"]
    process_orders(row)
    macd = row["macd"]
    process_macd_queue(macd)
    num_macds = macd_queue.qsize()
    if previous_macd_diff is not None:
        if is_macd_cross(current_macd_diff):
            if macd < 0:
                if not is_invested:
                    if row['Close'] > row['ema']:
                        if abs(macd) > (macd_sum / num_macds):
                            is_market_buy_order = True
            else:
                if is_invested:
                    if abs(macd) > (macd_sum / num_macds):
                        is_market_sell_order = True

    previous_macd_diff = current_macd_diff

print("cash " + str(cash))
print("return " + str((cash / 100000 -1) * 100))
print("orders " + str(orders))
print("wins " + str(wins))
print("losses " + str(losses))
print("win percentage " + str(0 if wins == 0 else total_win_percentage/wins))
print("loss_percentage " + str(0 if losses == 0 else total_loss_percentage/losses))
print(entry_date)
print("average trade days " + str(0 if orders ==0 else total_trade_days/orders))

