import tensorflow_ranking as tfr
import tensorflow_recommenders as tfrs
import numpy as np
import tensorflow as tf

class ListwiseModel(tfrs.Model):

    def __init__(self, loss):
        super().__init__()

        # Compute predictions.
        self.score_model = tf.keras.Sequential([
            # Learn multiple dense layers.
            tf.keras.layers.Dense(60, activation="relu"),
            tf.keras.layers.Dense(20, activation="relu"),
            # Make rating predictions in the final layer.
            tf.keras.layers.Dense(1)
        ])

        self.task = tfrs.tasks.Ranking(
            loss=loss,
            metrics=[
                tfr.keras.metrics.NDCGMetric(name="ndcg_metric"),
                tf.keras.metrics.RootMeanSquaredError()
            ]
        )

    def call(self, features):
        # [batch_size, num_of_stocks, features_dim]

        return self.score_model(features["features"])

    def compute_loss(self, features, training=False):
        labels = features.pop("labels")

        scores = self(features)

        return self.task(
            labels=labels,
            predictions=tf.squeeze(scores, axis=-1),
        )