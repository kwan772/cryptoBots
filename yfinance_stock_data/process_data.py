import os
import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine, text


class Process_data:

    @staticmethod
    def fetch_data():
        # Create a connection to your MySQL database
        num_of_stocks = 1475
        db_connection_str = 'mysql+pymysql://root:' + os.getenv('DB_PASSWORD') + '@localhost/stock_data'
        engine = create_engine(db_connection_str)
        query = text(
            "select close, Date, Symbol, volume, ema, rsi, macd, bollinger_high, bollinger_low, previous_day_change_percentage, next_day_change_percentage from new_stock_price order by date asc, symbol asc")

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            pd.set_option('display.max_columns', None)

            # Convert 'Date' to datetime if not already
            df['Date'] = pd.to_datetime(df['Date'])

            # Sort values by 'Symbol' and 'Date'
            df = df.sort_values(['Date', 'Symbol'])
            window_size = 7

            df.drop(['Symbol', 'Date', 'bollinger_high', 'bollinger_low'], axis=1, inplace=True)

            df_new = []
            train_sample = []
            label_sample = []
            count = 1

            for i in range(window_size * num_of_stocks + num_of_stocks * 37, len(df), num_of_stocks):
                one_day_train = []
                one_day_label = []
                print("processing day " + str(count))
                count += 1
                for k in range(0, num_of_stocks):
                    temp_train = []
                    temp_label = []
                    one_day_label.append(df.iloc[i + k]['next_day_change_percentage'])
                    for j in range(window_size, 0, -1):
                        row = df.iloc[i + k - num_of_stocks * j]
                        # temp_label.append(row['next_day_change_percentage'])
                        temp_train.append(row.drop(['next_day_change_percentage']).values)
                    one_day_train.append(temp_train)
                    # one_day_label.append(temp_label)

                train_sample.append(one_day_train)
                label_sample.append(one_day_label)

            train_sample = np.array(train_sample)
            label_sample = np.array(label_sample)
            original_label_sample = label_sample

            print(train_sample.shape)
            scaler = MinMaxScaler()
            train_sample_2d = train_sample.reshape(train_sample.shape[0], -1)
            label_sample_2d = label_sample

            for ir, r in enumerate(train_sample_2d):
                for ix, x in enumerate(r):
                    if np.isnan(x):
                        print(x)
                        print(ir)
                        print(ix)
                        print("train")

            scaler.fit(train_sample_2d)
            scaled_train_sample = scaler.fit_transform(train_sample_2d)
            scaled_label_sample = scaler.fit_transform(label_sample_2d)
            # train_sample = scaled_train_sample.reshape(train_sample.shape)
            # label_sample = scaled_label_sample.reshape(label_sample.shape)

            train_sample_length = len(train_sample)
            cut_of = round(train_sample_length * 0.8)

            # train = {'sample': train_sample[0: cut_of],
            #          'label': label_sample[0:cut_of]}
            # test = {'sample': train_sample[cut_of:],
            #         'label': label_sample[cut_of:]}
            # original_test_labels = original_label_sample[cut_of:]

            train = {'sample': scaled_train_sample[0: cut_of],
                     'label': scaled_label_sample[0:cut_of]}
            test = {'sample': scaled_train_sample[cut_of:],
                    'label': scaled_label_sample[cut_of:]}
            original_test_labels = original_label_sample[cut_of:]

            # with open('processed_stock_data.pickle', 'wb') as f:
            #     pickle.dump((train, test, original_test_labels), f)

            return train, test, original_test_labels
            # print(df_new)

            # for i in range(window_size, len(df_pivot)):
            #     # Get the last 'window_size' days of features for all stocks
            #     temp = df_pivot.iloc[i - window_size:i, :].values
            #
            #     # Append this data to new_data
            #     new_data.append(temp)
            #
            #
            # for data in new_data:
            #     for row in data:
            #         with np.printoptions(threshold=np.inf):
            #             print(row)
            # # Convert new_data to a numpy array
            # new_data = np.array(new_data)

    @staticmethod
    def calc_insert_price_percentage():
        # Create a connection to your MySQL database
        db_connection_str = 'mysql+pymysql://root:' + os.getenv('DB_PASSWORD') + '@localhost/stock_data'
        engine = create_engine(db_connection_str)

        with engine.connect() as conn:
            # Get unique symbols
            symbols = pd.read_sql(text("SELECT DISTINCT symbol FROM combined_twenty_year_stocks_with_indicators"), conn)
            # For each symbol, calculate the daily change percentage and update the database
            for symbol in symbols['symbol']:
                # Read data for one symbol
                query = text(
                    f"SELECT * FROM combined_twenty_year_stocks_with_indicators WHERE symbol='{symbol}' ORDER BY date")
                df = pd.read_sql(query, conn)

                print(df)

                # Calculate daily change percentage
                df['previous_day_change_percentage'] = df['Close'].pct_change() * 100
                df['next_day_change_percentage'] = df['Close'].shift(-1).pct_change() * 100

                # Write the updated data back to the database, replacing the existing data
                df.to_sql('new_stock_price', conn, if_exists='append', index=False)
                conn.commit()

            print("Update complete!")

    @staticmethod
    def load_processed_data():
        with open('processed_combined_stock_data.pickle', 'rb') as f:
            train, test, original_test_labels = pickle.load(f)
        return train, test, original_test_labels

    @staticmethod
    def load_processed_rank_data():
        with open('processed_stock_ranking_data_all_symbols.pickle', 'rb') as f:
            train, test, original_test_labels = pickle.load(f)
        return train, test, original_test_labels

    @staticmethod
    def process_ranking_data():
        # Create a connection to your MySQL database
        num_of_stocks = 1475
        db_connection_str = 'mysql+pymysql://root:' + os.getenv('DB_PASSWORD') + '@localhost/stock_data'
        engine = create_engine(db_connection_str)
        input_dim = 134225

        with engine.connect() as conn:
            query = text(f'''
            CREATE TEMPORARY TABLE temp_stocks_ranked AS
            SELECT 
              id as new_id, 
              date(date) as d, 
              RANK() OVER (
                PARTITION BY date(date)
                ORDER BY `next_day_change_percentage` DESC
              ) AS ranking
            FROM new_stock_price;
            ''')
            conn.execute(query)
            conn.commit()

        query = text(
            f'''
            SELECT * from new_stock_price a
            JOIN temp_stocks_ranked b 
            ON a.id = b.new_id
            WHERE macd is not null''')

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            pd.set_option('display.max_columns', None)

            # Sort values by 'Symbol' and 'Date'
            df = df.sort_values(['d', 'Symbol'])
            window_size = 7
            print(df.columns)
            df.drop(['Symbol', 'Date', 'Bollinger_High', 'Bollinger_Low','id', 'Dividends', 'Stock Splits', 'rank', 'd', 'new_id'], axis=1, inplace=True)



            train_sample = []
            label_sample = []
            count = 1

            cols_to_scale = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA', 'EMA', 'RSI', 'MACD', 'Stoch_Oscillator', 'ADX', 'MFI', 'previous_day_change_percentage', 'ranking']

            # Initialize a scaler
            scaler = MinMaxScaler()

            # Scale the columns
            df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])



            for i in range(window_size * num_of_stocks, len(df), num_of_stocks):
                one_day_train = []
                one_day_label = []
                print("processing day " + str(count))
                count += 1
                for k in range(0, num_of_stocks):
                    temp_train = []
                    one_day_label.append(df.iloc[i + k]['ranking'])
                    for j in range(window_size, 0, -1):
                        row = df.iloc[i + k - num_of_stocks * j]
                        # temp_label.append(row['next_day_change_percentage'])
                        temp_train.append(row.drop(['next_day_change_percentage','ranking']).values)
                    one_day_train.append(temp_train)
                    # one_day_label.append(temp_label)

                train_sample.append(one_day_train)
                label_sample.append(one_day_label)

            train_sample = np.array(train_sample)
            label_sample = np.array(label_sample)
            original_label_sample = label_sample

            train_sample = train_sample.reshape(train_sample.shape[0], -1)

            print(train_sample)
            print(label_sample)
            print(train_sample.shape)
            print(label_sample.shape)

            with open('processed_stock_ranking_data_all_symbols.pickle', 'wb') as f:
                pickle.dump((train_sample, label_sample, original_label_sample), f)


if __name__ == "__main__":
    Process_data.process_ranking_data()
    # Process_data.calc_insert_price_percentage()
