import os
import pickle

import numpy as np
from sqlalchemy import create_engine, text
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
class Data_processor:
    @staticmethod
    def process_data():
        stocks = ['AAPL', 'AMD', 'ASML', 'MSFT', 'FDX']
        db_connection_str = "mysql+pymysql://root:" + os.getenv('DB_PASSWORD') + "@localhost/stock_data"
        engine = create_engine(db_connection_str)
        stocks_str = "','".join(stocks)
        query = text(f"select open, high, low, close, volume, symbol, sma, ema, rsi, macd, bollinger_high, bollinger_low, stoch_oscillator, adx, mfi, `previous_day_change_percentage`, `next_day_change_percentage`, date(Date) dutc from new_stock_price where symbol in ('{stocks_str}') and macd is not null order by dutc asc, Symbol asc")

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            # Select columns to scale
            cols_to_scale = ['open', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi', 'macd', 'bollinger_high', 'bollinger_low', 'stoch_oscillator', 'adx', 'mfi', 'previous_day_change_percentage']

            # Initialize a scaler
            scaler = MinMaxScaler()

            # Scale the columns
            df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

        inputs1 = []
        inputs2 = []
        labels = []
        sliding_window = 7
        day = 0

        for i in range(len(stocks)*sliding_window, len(df)-len(stocks), len(stocks)):
            day+=1
            print("day processed " + str(day))
            for j in range(0, len(stocks)):
                for k in range(j+1, len(stocks)):
                    input1 = []
                    input2 = []
                    label = df.loc[i+j]['next_day_change_percentage']-df.loc[i+k]['next_day_change_percentage']
                    for h in range(sliding_window, -1, -1):
                        # print(df.loc[i+j-h*len(stocks)]['symbol'] + '===============' + df.loc[i+k-h*len(stocks)]['symbol'] + " day" + str(h))
                        input1.append(df.loc[i+j-h*len(stocks)][['open', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi', 'macd', 'bollinger_high', 'bollinger_low', 'stoch_oscillator', 'adx', 'mfi', 'previous_day_change_percentage']].values)
                        input2.append(df.loc[i+k-h*len(stocks)][['open', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi', 'macd', 'bollinger_high', 'bollinger_low', 'stoch_oscillator', 'adx', 'mfi', 'previous_day_change_percentage']].values)
                        # break
                    inputs1.append(input1)
                    inputs2.append(input2)
                    labels.append([1 if label > 0 else 0])
            #         break
            #     break
            # break
        # print(inputs1)
        # print(inputs2)
        print(labels)
        inputs1 = np.array(inputs1)
        inputs2 = np.array(inputs2)
        labels = np.array(labels)

        with open('processed_stock_data_5_symbols.pickle', 'wb') as f:
            pickle.dump((inputs1, inputs2, labels), f)

    @staticmethod
    def process_data_linear_model():
        stocks = 6
        db_connection_str = "mysql+pymysql://root:" + os.getenv('DB_PASSWORD') + "@localhost/stock_data"
        engine = create_engine(db_connection_str)
        query = text(
            f"""
            select open, high, low, close, volume, symbol, sma, ema, rsi, macd, bollinger_high, bollinger_low, stoch_oscillator, adx, mfi, `previous_day_change_percentage`, `next_day_change_percentage`, date(Date) dutc from new_stock_price where macd is not null and symbol in ("aapl", "msft", "aig", "hsic", "ibm","intc") order by dutc asc, Symbol asc limit 14580""")

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            # Select columns to scale
            cols_to_scale = ['open', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi', 'macd', 'bollinger_high',
                             'bollinger_low', 'stoch_oscillator', 'adx', 'mfi', 'previous_day_change_percentage']

            # Initialize a scaler
            scaler = MinMaxScaler()

            # Scale the columns
            df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

        inputs1 = []
        inputs2 = []
        labels = []
        sliding_window = 7
        day = 0

        for i in range(stocks * sliding_window, len(df) - stocks, stocks):
            day += 1
            print("day processed " + str(day))
            for j in range(0, stocks):
                for k in range(j + 1, stocks):
                    input1 = []
                    input2 = []
                    label = df.loc[i + j]['next_day_change_percentage'] - df.loc[i + k]['next_day_change_percentage']
                    for h in range(sliding_window, -1, -1):
                        # print(df.loc[i+j-h*len(stocks)]['symbol'] + '===============' + df.loc[i+k-h*len(stocks)]['symbol'] + " day" + str(h))
                        input1.extend(df.loc[i + j - h * stocks][
                                          ['open', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi', 'macd',
                                           'bollinger_high', 'bollinger_low', 'stoch_oscillator', 'adx', 'mfi',
                                           'previous_day_change_percentage']].values)
                        input2.extend(df.loc[i + k - h * stocks][
                                          ['open', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi', 'macd',
                                           'bollinger_high', 'bollinger_low', 'stoch_oscillator', 'adx', 'mfi',
                                           'previous_day_change_percentage']].values)
                        # break
                    inputs1.append(input1)
                    inputs2.append(input2)
                    labels.append([1 if label > 0 else 0])
            #         break
            #     break
            # break
        print(inputs1)
        print(inputs2)
        print(labels)
        inputs1 = np.array(inputs1)
        inputs2 = np.array(inputs2)
        labels = np.array(labels)
        print(inputs1.shape)
        print(inputs2.shape)
        print(labels.shape)

        with open('processed_stock_data_all_symbols_linear_model.pickle', 'wb') as f:
            pickle.dump((inputs1, inputs2, labels), f)

    @staticmethod
    def load_processed_data():
        with open('processed_stock_data_5_symbols.pickle', 'rb') as f:
            inputs1, inputs2, labels = pickle.load(f)
        return inputs1, inputs2, labels

    @staticmethod
    def load_linear_processed_data():
        with open('processed_stock_data_all_symbols_linear_model.pickle', 'rb') as f:
            inputs1, inputs2, labels = pickle.load(f)
        return inputs1, inputs2, labels


if __name__ == "__main__":
    Data_processor.process_data_linear_model()