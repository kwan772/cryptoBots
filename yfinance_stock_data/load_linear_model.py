import pickle

import numpy as np
import tensorflow as tf
from stock_LSTM_model import RankingModel
import tensorflow_ranking as tfr
from process_data import Process_data
from linear_model import LinearModelLocal

if __name__ == "__main__":
    sample, label, original_test = Process_data.load_processed_rank_data()
    print("loaded data")
    with tf.device('/cpu:0'):
        loaded_model = tf.keras.models.load_model('linear_model', custom_objects={
            'LinearModelLocal': LinearModelLocal
        })
        print("predicting")

        pred_sample = sample[0:3]
        pred_label = label[0:3]

        predictions = loaded_model.predict(pred_sample, verbose=0)

        for index, prediction in enumerate(predictions):
            for p in prediction:
                print(p)
            print(pred_label[index])
            print(pred_sample[index])
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')