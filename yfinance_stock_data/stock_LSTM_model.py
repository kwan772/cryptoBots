import tensorflow as tf

import tensorflow_ranking as tfr
import tensorflow_recommenders as tfrs

class RankingModel(tfrs.Model):

    def __init__(self, loss):
        super().__init__()
        stockNumber = 1475
        self.loss = loss

        # self.score_model = tf.keras.Sequential([
        #     # Learn multiple dense layers.
        #     # tf.keras.layers.Dense(round(stockNumber + stockNumber * (30)), activation="relu"),
        #     # tf.keras.layers.Dense(round(stockNumber + stockNumber * (20)), activation="relu"),
        #     # tf.keras.layers.Dense(round(stockNumber + stockNumber * (10)), activation="relu"),
        #     tf.keras.layers.Dense(round(stockNumber + stockNumber * (5)), activation="relu"),
        #     tf.keras.layers.Dense(round(stockNumber + stockNumber * (5)), activation="relu"),
        #     tf.keras.layers.Dense(round(stockNumber + stockNumber * (3)), activation="relu"),
        #     tf.keras.layers.Dense(round(stockNumber + stockNumber * (1)), activation="relu"),
        #     tf.keras.layers.Dense(round(stockNumber + stockNumber * (1/3)), activation="relu"),
        #     # Make rating predictions in the final layer.
        #     # tf.keras.layers.Dense(stockNumber)
        #
        #
        #     # Learn multiple dense layers.
        #     # tf.keras.layers.Dense(round(stockNumber + stockNumber * (2 / 3))),
        #     # tf.keras.layers.BatchNormalization(),  # Batch Normalization layer
        #     # tf.keras.layers.Activation('relu'),
        #     #
        #     # tf.keras.layers.Dense(round(stockNumber + stockNumber * (1 / 3))),
        #     # tf.keras.layers.BatchNormalization(),  # Batch Normalization layer
        #     # tf.keras.layers.Activation('relu'),
        #
        #     # Make rating predictions in the final layer.
        #     tf.keras.layers.Dense(stockNumber, activation="sigmoid")
        # ])

        self.score_model = tf.keras.Sequential([
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (5)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (5)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (3)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (1)), activation="relu"),
            tf.keras.layers.Dense(round(stockNumber + stockNumber * (1 / 3)), activation="relu"),
            tf.keras.layers.Dense(stockNumber, activation="linear")  # Changed activation to linear
        ])

        self.task = tfrs.tasks.Ranking(
            loss=self.loss,
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
        features = features[0]
        # print(features)
        labels = features.pop("label")

        scores = self(features)

        # print(scores)
        # print(labels)

        return self.task(
            labels=labels,
            predictions=scores,
        )

    def get_config(self):
        config = super(RankingModel, self).get_config()
        config.update({
            'loss': self.loss,
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)
