import pickle

import numpy as np
import tensorflow as tf
from stock_LSTM_model import RankingModel
import tensorflow_ranking as tfr
from process_data import Process_data

train, test, original_test = Process_data.load_processed_data()
print("loading data")
with tf.device('/cpu:0'):
    loaded_model = tf.keras.models.load_model('listwise_model_all_days_tensorflow', custom_objects={
        'RankingModel': RankingModel,
        # 'ListMLELoss': tfr.keras.losses.ListMLELoss,
        # 'NDCGMetric': tfr.keras.metrics.NDCGMetric,
        'NDCGMetric': tfr.keras.losses.PairwiseHingeLoss(),
    })
    print("predicting")

    lwpredictions = loaded_model.predict(test, verbose=0)
    sums = []
    orders = []
    symbol_indexes = []
    for index, prediction in enumerate(lwpredictions):
        # print(prediction.argsort()[-10:])
        # print("==========================")
        # print(prediction[prediction.argsort()[-10:]])
        # print(test['label'][index][prediction.argsort()[-10:]])
        # print("==========================")
        sum = original_test[index][prediction.argsort()[-5:]].sum()
        # print(sum)
        sums.append(sum)
        symbol_indexes.append(prediction.argsort()[-5:])
        print(prediction[prediction.argsort()[-5:]])
        print(prediction.argsort()[-5:])
        print(original_test[index].argsort()[-5:])
        print(prediction[prediction.argsort()[-5:]])
        arr = original_test[index].argsort()
        rankings = np.array([np.where(arr == i) for i in prediction.argsort()[-5:]])
        order = rankings.sum() / 5
        orders.append(order)
        print(rankings)
        print(test['sample'][index])
        print(test['label'][index])
        print("@@@@@@@@@@@@@@@@@@@@@@@")

    sums = np.array(sums)
    orders = np.array(orders)
    # print(sums.shape)
    print(sums.sum() / sums.shape[0])
    print(orders.sum() / orders.shape[0])
    # 13%