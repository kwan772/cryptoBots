import tensorflow as tf
import tensorflow_ranking as tfr
from linear_model import LinearModelLocal
from process_data import Process_data
import numpy as np
from tensorflow.keras.callbacks import TensorBoard
import pickle
import os

if __name__ == "__main__":
    # StockData.getAllPriceData()
    # StockData.cutTimeCSV()
    # StockData.updatePriceChange()
    #StockData.combinePriceData(2513)
    with tf.device('/cpu:0'):
        process_data = Process_data()
        train,test, original_test = process_data.test_process_ranking_data()
        # os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
        # train,test, original_test = process_data.fetch_data()
        tensorboard_callback = TensorBoard(log_dir="./logs")
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',  # The metric to monitor
            patience=3,  # Number of epochs with no improvement to wait
            mode='min'  # Training will stop when the quantity monitored has stopped decreasing
        )
        print("FEATURE DIM " + str(train.shape[1]))
        linear_model = LinearModelLocal()
        # Compile the model
        linear_model.compile(optimizer='adam', loss='mse')
        # Fit the model
        linear_model.fit(train, test, epochs=10, batch_size=256, verbose=2,
                  callbacks=[tensorboard_callback],
                  validation_split=0.1)

        # Specify GPU device
        # gpus = tf.config.experimental.list_physical_devices('GPU')
        # tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
        # tfr.keras.losses.ListMLELoss()
        # listwise_model = RankingModel(tf.keras.losses.MeanSquaredError())
        # listwise_model = RankingModel(tfr.keras.losses.ListMLELoss())
        # listwise_model = RankingModel(tfr.keras.losses.PairwiseHingeLoss())

        # listwise_model.compile(optimizer=tf.keras.optimizers.Adam())
        # linear_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.01))
        # linear_model.fit(train, epochs=100, batch_size=256, verbose=2, callbacks=[tensorboard_callback], validation_split=0.1)

        # linear_model_result = linear_model.evaluate(test, return_dict=True)
        # print(linear_model_result)
        # print("NDCG of the ListMLE model: {:.4f}".format(listwise_model_result["ndcg_metric"]))

        # lwpredictions = linear_model.predict(test, verbose=0)
        # sums = []
        # for index, prediction in enumerate(lwpredictions):
        #     # print(prediction.argsort()[-10:])
        #     # print("==========================")
        #     # print(prediction[prediction.argsort()[-10:]])
        #     # print(test['label'][index][prediction.argsort()[-10:]])
        #     # print("==========================")
        #     sum = original_test[index][prediction.argsort()[-5:]].sum()
        #     # print(sum)
        #     sums.append(sum)
        #
        # sums = np.array(sums)
        # # print(sums.shape)
        # print(sums.sum() / sums.shape[0])

        linear_model.save('linear_model')
        # pickle.dump(listwise_model, open("listwise_model_all_days.pkl", "wb"))