import tensorflow as tf
from tensorflow.keras.layers import Dense, Subtract, Dropout
from tensorflow.keras.models import Model

class LinearModelLocal(Model):
    def __init__(self):
        super(LinearModelLocal, self).__init__()
        stockNumber = 1458

        # self.dense1 = Dense(round(stockNumber + stockNumber * (30)), activation="relu")
        # # self.dropout1 = Dropout(0.5)
        # self.dense2 = Dense(round(stockNumber + stockNumber * (20)), activation="relu")
        # # self.dropout2 = Dropout(0.5)
        # # self.dense3 = Dense(round(stockNumber + stockNumber * (10)), activation="relu")
        # # self.dropout3 = Dropout(0.5)
        # self.dense4 = Dense(round(stockNumber + stockNumber * (5)), activation="relu")
        # # self.dropout4 = Dropout(0.5)
        # # self.dense5 = Dense(round(stockNumber + stockNumber * (2)), activation="relu")
        # # self.dropout5 = Dropout(0.5)
        # self.dense6 = Dense(round(stockNumber + stockNumber * (1)), activation="relu")
        # # self.dense7 = Dense(round(stockNumber + stockNumber * (1/2)), activation="relu")
        # self.dense8 = Dense(round(stockNumber), activation="relu")
        self.score_model = tf.keras.Sequential([
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (5)), activation="relu"),
            # tf.keras.layers.Dense(round(stockNumber + stockNumber * (5)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (3)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (1)), activation="relu"),
            # tf.keras.layers.Dense(round(stockNumber + stockNumber * (1 / 3)), activation="relu"),
            # tf.keras.layers.Dense(stockNumber, activation="relu")  # Changed activation to linear
            tf.keras.layers.Dense(1, activation="relu")  # Changed activation to linear
        ])


    def call(self, inputs):
        # # Get the output for the first set of inputs
        # x1 = self.dense1(inputs)
        # # x1 = self.dropout1(x1)
        # x1 = self.dense2(x1)
        # # x1 = self.dropout2(x1)
        # # x1 = self.dense3(x1)
        # # x1 = self.dropout3(x1)
        # x1 = self.dense4(x1)
        # # x1 = self.dropout4(x1)
        # # x1 = self.dense5(x1)
        # # x1 = self.dropout5(x1)
        # x1 = self.dense6(x1)
        # # x1 = self.dense7(x1)
        # x1 = self.dense8(x1)

        return self.score_model(inputs)
