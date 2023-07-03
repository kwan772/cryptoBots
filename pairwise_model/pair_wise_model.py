import tensorflow as tf
from tensorflow.keras.layers import Dense, Subtract, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers

class PairwiseRankingModel(Model):
    def __init__(self, feature_dim):
        super(PairwiseRankingModel, self).__init__()

        self.dense1 = Dense(120, activation='relu')
        self.dropout1 = Dropout(0.5)
        self.dense2 = Dense(90, activation='relu')
        self.dropout2 = Dropout(0.5)
        self.dense3 = Dense(60, activation='relu')
        self.dropout3 = Dropout(0.5)
        self.dense4 = Dense(30, activation='relu')
        self.dropout4 = Dropout(0.5)
        self.dense5 = Dense(10, activation='relu')
        self.dropout5 = Dropout(0.5)
        self.dense6 = Dense(1)

    def call(self, inputs):
        # Separate the inputs into two sets
        input1, input2 = inputs

        # Get the output for the first set of inputs
        x1 = self.dense1(input1)
        x1 = self.dropout1(x1)
        x1 = self.dense2(x1)
        x1 = self.dropout2(x1)
        x1 = self.dense3(x1)
        x1 = self.dropout3(x1)
        x1 = self.dense4(x1)
        x1 = self.dropout4(x1)
        x1 = self.dense5(x1)
        x1 = self.dropout5(x1)
        x1 = self.dense6(x1)

        # Get the output for the second set of inputs
        x2 = self.dense1(input2)
        x2 = self.dropout1(x2)
        x2 = self.dense2(x2)
        x2 = self.dropout2(x2)
        x2 = self.dense3(x2)
        x2 = self.dropout3(x2)
        x2 = self.dense4(x2)
        x2 = self.dropout4(x2)
        x2 = self.dense5(x2)
        x2 = self.dropout5(x2)
        x2 = self.dense6(x2)

        # Compute the difference in scores
        diff = Subtract()([x1, x2])

        return diff
