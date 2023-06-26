import pprint
import pandas as pd

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

import tensorflow_ranking as tfr
import tensorflow_recommenders as tfrs
from sklearn.preprocessing import MinMaxScaler

# ratings = tfds.load("movielens/100k-ratings", split="train")
# movies = tfds.load("movielens/100k-movies", split="train")
#
# ratings = ratings.map(lambda x: {
#     "movie_title": x["movie_title"],
#     "user_id": x["user_id"],
#     "user_rating": x["user_rating"],
# })
# movies = movies.map(lambda x: x["movie_title"])
#
# unique_movie_titles = np.unique(np.concatenate(list(movies.batch(1000))))
# unique_user_ids = np.unique(np.concatenate(list(ratings.batch(1_000).map(
#     lambda x: x["user_id"]))))

if __name__ == '__main__':

    df = pd.read_csv("combined.csv")

    train_labels = []
    train_samples = []
    row = 0

    for i in range(0, 912):
        sample = []
        market_cap = []
        label = []
        for j in range(0,102):
            sample.append(df.iloc[row]['Pre Change'])
            market_cap.append(df.iloc[row]['market_cap']/787437397453.93)
            label.append(df.iloc[row]['Post Change'])
            row+=1
        sample = sample + market_cap
        train_samples.append(sample)
        train_labels.append(label)


    print(len(train_samples),len(train_samples[0]))
    print(len(train_labels),len(train_labels[0]))

    train_samples = np.array(train_samples)
    train_labels = np.array(train_labels)

    # scaler = MinMaxScaler(feature_range=(-1,1))
    # scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1,1))
    # testscaled_train_samples = scaled_train_samples.reshape(842,276)
    #
    # print(len(scaled_train_samples))

    train = {'sample':train_samples[0:912], 'label':train_labels[0:912]}
    test = {'sample':train_samples[820:912], 'label':train_labels[820:912]}


    class RankingModel(tfrs.Model):

        def __init__(self, loss):
            super().__init__()

            # Compute predictions.
            self.score_model = tf.keras.Sequential([
                # Learn multiple dense layers.
                tf.keras.layers.Dense(184, activation="relu"),
                tf.keras.layers.Dense(150, activation="relu"),
                # Make rating predictions in the final layer.
                tf.keras.layers.Dense(102)
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
            features = features[0]
            labels = features.pop("label")

            scores = self(features)

            # print(scores)
            # print(labels)

            return self.task(
                labels=labels,
                predictions=scores,
            )


    listwise_model = RankingModel(tfr.keras.losses.ListMLELoss())
    listwise_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    listwise_model.fit(train, epochs=10, verbose=0)

    mse_model = RankingModel(tf.keras.losses.MeanSquaredError())
    mse_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    mse_model.fit(train, epochs=10, verbose=0)

    hinge_model = RankingModel(tfr.keras.losses.PairwiseHingeLoss())
    hinge_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    hinge_model.fit(train, epochs=10, verbose=0)

    mse_model_result = mse_model.evaluate(test, return_dict=True)
    print("NDCG of the mse model: {:.4f}".format(mse_model_result["ndcg_metric"]))

    hinge_model_result = hinge_model.evaluate(test, return_dict=True)
    print("NDCG of the hinge model: {:.4f}".format(hinge_model_result["ndcg_metric"]))

    listwise_model_result = listwise_model.evaluate(test, return_dict=True)
    print("NDCG of the ListMLE model: {:.4f}".format(listwise_model_result["ndcg_metric"]))

    mspredictions = mse_model.predict(test,verbose=0)
    sums = []
    for index,prediction in enumerate(mspredictions):
        # print(prediction.argsort()[-10:])
        # print(prediction[prediction.argsort()[-10:]])
        # print(test['label'][index][prediction.argsort()[-10:]])
        sum = test['label'][index][prediction.argsort()[-10:]].sum()
        # print(sum)
        sums.append(sum)

    sums = np.array(sums)
    # print(sums.shape)
    print(sums.sum()/sums.shape[0])

    hgpredictions = hinge_model.predict(test, verbose=0)
    sums = []
    for index, prediction in enumerate(hgpredictions):
        # print(prediction.argsort()[-10:])
        # print(prediction[prediction.argsort()[-10:]])
        # print(test['label'][index][prediction.argsort()[-10:]])
        sum = test['label'][index][prediction.argsort()[-10:]].sum()
        # print(sum)
        sums.append(sum)

    sums = np.array(sums)
    # print(sums.shape)
    print(sums.sum() / sums.shape[0])

    lwpredictions = listwise_model.predict(test, verbose=0)
    sums = []
    for index, prediction in enumerate(lwpredictions):
        # print(prediction.argsort()[-10:])
        # print(prediction[prediction.argsort()[-10:]])
        # print(test['label'][index][prediction.argsort()[-10:]])
        sum = test['label'][index][prediction.argsort()[-10:]].sum()
        # print(sum)
        sums.append(sum)

    sums = np.array(sums)
    # print(sums.shape)
    print(sums.sum() / sums.shape[0])


    # all_sums = []
    # for i in range(0,len(lwpredictions)):
    #     msp = mspredictions[i].argsort()[-10:]
    #     hgp = hgpredictions[i].argsort()[-10:]
    #     lwp = lwpredictions[i].argsort()[-10:]
    #     print(msp)
    #     print(lwp)
    #     #selections = np.intersect1d(msp, lwp)
    #     selections = []
    #     for x in lwp:
    #         if mspredictions[i][x] >0:
    #             selections.append(x)
    #     print("#################################")
    #     print(test['label'][i][selections])
    #     all_sum = test['label'][i][selections].sum()
    #     all_sums.append(all_sum)
    #
    # all_sums = np.array(all_sums)
    # print(all_sums.sum()/all_sums.shape[0])
