import os
import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine, text
import tensorflow as tf


class DataProcessor:

    @staticmethod
    def process_ranking_data():
        # Create a connection to your MySQL database
        num_of_stocks = 6
        db_connection_str = 'mysql+pymysql://root:' + os.getenv('DB_PASSWORD') + '@localhost/stock_data'
        engine = create_engine(db_connection_str)

        query = text(
            f"""
                select open, high, low, close, volume, symbol, sma, ema, rsi, macd, bollinger_high, bollinger_low, stoch_oscillator, adx, mfi, `previous_day_change_percentage`, `next_day_change_percentage`, date(Date) d from stock_price_with_rankings where macd is not null and symbol in ("aapl", "msft", "aig", "hsic", "ibm","intc") order by d asc, Symbol asc limit 600
            """)

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            pd.set_option('display.max_columns', None)

            # Sort values by 'Symbol' and 'Date'
            df = df.sort_values(['d', 'symbol'])
            window_size = 7
            # df.drop(['Symbol', 'Date', 'id', 'Dividends', 'Stock Splits', 'd', 'Open', 'High', 'Low', 'SMA',
            #          'Stoch_Oscillator', 'ADX', 'MFI', 'next_day_change_percentage'], axis=1, inplace=True)
            df.drop(['symbol', 'd'], axis=1, inplace=True)
            print(df.columns)

            train_sample = []
            label_sample = []
            count = 1

            cols_to_scale = ['open','close', 'high', 'low', 'sma', 'stoch_oscillator', 'adx', 'mfi', 'volume', 'ema', 'rsi', 'macd', 'previous_day_change_percentage',
                             'bollinger_high', 'bollinger_low']

            # Initialize a scaler
            scaler = MinMaxScaler()

            # Scale the columns
            df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

            # [num_samples, num_of_stocks, feature_dim]
            # [num_samples, num_ofs

            for i in range(window_size * num_of_stocks, len(df), num_of_stocks):
                one_day_label = []
                one_day_train = []
                print("processing day " + str(count))
                count += 1
                for k in range(0, num_of_stocks):
                    temp_train = []
                    one_day_label.append(df.iloc[i + k]['next_day_change_percentage'])
                    for j in range(window_size, -1, -1):
                        row = df.iloc[i + k - num_of_stocks * j]
                        temp_train.extend(row.drop(['next_day_change_percentage']).values)
                    one_day_train.append(temp_train)

                train_sample.append(one_day_train)
                label_sample.append(one_day_label)

            # train_sample = np.array(train_sample)
            # label_sample = np.array(label_sample)

            # Convert the lists or arrays to TensorFlow tensors
            # features = tf.convert_to_tensor(train_sample, dtype=tf.float32)
            # labels = tf.convert_to_tensor(label_sample, dtype=tf.float32)

            # Create a tf.data.Dataset
            # dataset = tf.data.Dataset.from_tensor_slices({
            #     'features': features,
            #     'labels': labels
            # })


            # print(train_sample)
            # print(label_sample)
            # print(train_sample.shape)
            # print(label_sample.shape)

            # print(dataset)

            with open('ranking_data.pickle', 'wb') as f:
                pickle.dump((train_sample, label_sample), f)
                print("saved")

    @staticmethod
    def load_rank_data():
        # Load the data from the pickle file
        with open('ranking_data.pickle', 'rb') as f:
            train_sample, label_sample = pickle.load(f)

            # Convert the lists or arrays to TensorFlow tensors
            features = tf.convert_to_tensor(train_sample, dtype=tf.float32)
            labels = tf.convert_to_tensor(label_sample, dtype=tf.float32)

            # Create a tf.data.Dataset
            dataset = tf.data.Dataset.from_tensor_slices({
                'features': features,
                'labels': labels
            })

            return dataset


if __name__ == "__main__":
    DataProcessor.process_ranking_data()