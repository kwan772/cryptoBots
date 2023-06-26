import numpy
import pandas as pd

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

import tensorflow_ranking as tfr
import tensorflow_recommenders as tfrs
from sklearn.preprocessing import MinMaxScaler

stockNumber = 806
numberOfDays = 2513
# numberOfDays = 10
class StockPriceModel:

    priceDataFileName = "./stockData/combined2513days.parquet"

    def processData(self):

        #numberOfDays = 2513
        df = pd.read_parquet(self.priceDataFileName)

        train_labels = []
        train_samples = []
        row = 0

        #berkshire hathway -> stock with highest price
        MAX_STOCK_PRICE = 600000

        max_change = df.iloc[0]['Pre Change']
        for i in range(0, numberOfDays):
            sample = []
            market_cap = []
            label = []
            for j in range(0, stockNumber):
                if abs(df.iloc[row]['Pre Change']) > max_change:
                    max_change = df.iloc[row]['Pre Change']
                sample.append(df.iloc[row]['Pre Change'])
                # market_cap.append(df.iloc[row]['market_cap'] / MAX_STOCK_PRICE)
                label.append(df.iloc[row]['Post Change'])
                row += 1
            # sample = sample + market_cap
            train_samples.append(sample)
            train_labels.append(label)
            # print("sample: " + str(sample) + " label:" + str(label))

        # for x in range(0, len(train_samples)):
        #     for y in range(0, stockNumber):
        #         train_samples[x][y] = train_samples[x][y] / max_change

        good = True
        for x in range(0, len(train_samples)):
            for y in train_samples[x]:
                if np.isnan(y) or np.isinf(y):
                    # print("sample wrong values@@@@@@@@@@@@@@@@")
                    # print(x)
                    # print(y)
                    good = False
        for x in range(0, len(train_labels)):
            for y in train_labels[x]:
                if np.isnan(y) or np.isinf(y):
                    # print("sample wrong values@@@@@@@@@@@@@@@@")
                    # print(x)
                    # print(y)
                    good = False

        if not good:
            return []

        # for x in train_labels:
        #     for y in x:
        #         if abs(y) > 1:
        #             # print("label wrong values@@@@@@@@@@@@@@@@")
        #             # print(y)
        #             good = False

        # if good:
        #     print("all within 1@@@@@@@@@@@@@@@@")
        # else:
        #     print("wrong values@@@@@@@@@@@@@@@@")
        #     print(max_change)

        # print(len(train_samples),len(train_samples[0]))
        # print(len(train_labels),len(train_labels[0]))

        train_samples = np.array(train_samples)
        train_labels = np.array(train_labels)

        scaler = MinMaxScaler(feature_range=(-1,1))
        scaled_train_samples = scaler.fit_transform(train_samples)
        scaled_train_labels = scaler.fit_transform(train_labels)
        train_samples = scaled_train_samples
        original_train_labels = train_labels
        train_labels = scaled_train_labels
        # testscaled_train_samples = scaled_train_samples.reshape(842,276)
        #
        # print(len(scaled_train_samples))

        print(train_samples[0])
        print(train_labels[0])
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        # train = {'sample': train_samples[0:round(len(train_samples)*0.9)], 'label': train_labels[0:round(len(train_labels)* 0.9)]}
        # test = {'sample': train_samples[round(len(train_samples)*0.9):len(train_samples)], 'label': train_labels[round(len(train_labels)* 0.9):len(train_labels)]}
        # original_test_labels = original_train_labels[round(len(train_labels)* 0.9):len(train_labels)]

        train = {'sample': train_samples[round(len(train_samples) * 0.2):],
                 'label': train_labels[round(len(train_labels) * 0.2):]}
        test = {'sample': train_samples[0:round(len(train_samples) * 0.2)],
                'label': train_labels[0:round(len(train_labels) * 0.2)]}
        original_test_labels = original_train_labels[0:round(len(train_labels) * 0.2)]
        return train, test, original_test_labels

class RankingModel(tfrs.Model):

    def __init__(self, loss):
        super().__init__()

        # Compute predictions.
        self.score_model = tf.keras.Sequential([
            # Learn multiple dense layers.
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (2/3)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (2/3)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (2/3)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (2/3)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (1/3)), activation="relu"),
            # Make rating predictions in the final layer.
            # tf.keras.layers.Dense(stockNumber)


            # Learn multiple dense layers.
            # tf.keras.layers.Dense(round(stockNumber + stockNumber * (2 / 3))),
            # tf.keras.layers.BatchNormalization(),  # Batch Normalization layer
            # tf.keras.layers.Activation('relu'),
            #
            # tf.keras.layers.Dense(round(stockNumber + stockNumber * (1 / 3))),
            # tf.keras.layers.BatchNormalization(),  # Batch Normalization layer
            # tf.keras.layers.Activation('relu'),

            # Make rating predictions in the final layer.
            tf.keras.layers.Dense(stockNumber, activation="sigmoid")
        ])

        self.task = tfrs.tasks.Ranking(
            loss=loss,
            metrics=[
                tfr.keras.metrics.NDCGMetric(name="ndcg_metric"),
                tf.keras.metrics.RootMeanSquaredError()
            ]
        )

    def call(self, features):
        # print(features,"!!!!!!!!!!!!")
        return self.score_model(features['sample'])

    def compute_loss(self, features, training=False):
        # print(features,"@@@@@@@@@@@@@@@")
        print(features)
        features = features[0]
        labels = features.pop("label")

        scores = self(features)

        # print(scores)
        # print(labels)

        return self.task(
            labels=labels,
            predictions=scores,
        )