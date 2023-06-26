from StockData import StockData
from StockPriceModel import  RankingModel
from StockPriceModel import  StockPriceModel
import tensorflow as tf
import tensorflow_ranking as tfr
import numpy as np
from tensorflow.keras.callbacks import TensorBoard


if __name__ == "__main__":
    # StockData.getAllPriceData()
    # StockData.cutTimeCSV()
    # StockData.updatePriceChange()
    #StockData.combinePriceData(2513)

    priceModel = StockPriceModel()
    train,test, original_test = priceModel.processData()
    tensorboard_callback = TensorBoard(log_dir="./logs")
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  # The metric to monitor
        patience=3,  # Number of epochs with no improvement to wait
        mode='min'  # Training will stop when the quantity monitored has stopped decreasing
    )
    # tfr.keras.losses.ListMLELoss()
    # listwise_model = RankingModel(tf.keras.losses.MeanSquaredError())
    listwise_model = RankingModel(tfr.keras.losses.ListMLELoss())
    # listwise_model.compile(optimizer=tf.keras.optimizers.Adam())
    listwise_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    listwise_model.fit(train, epochs=2000, verbose=2, callbacks=[tensorboard_callback], validation_data=test)

    # mse_model = RankingModel(tf.keras.losses.MeanSquaredError())
    # mse_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    # mse_model.fit(train, epochs=10, verbose=0)
    #
    # hinge_model = RankingModel(tfr.keras.losses.PairwiseHingeLoss())
    # hinge_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    # hinge_model.fit(train, epochs=10, verbose=0)
    #
    # mse_model_result = mse_model.evaluate(test, return_dict=True)
    # print("NDCG of the mse model: {:.4f}".format(mse_model_result["ndcg_metric"]))
    #
    # hinge_model_result = hinge_model.evaluate(test, return_dict=True)
    # print("NDCG of the hinge model: {:.4f}".format(hinge_model_result["ndcg_metric"]))

    listwise_model_result = listwise_model.evaluate(test, return_dict=True)
    print("NDCG of the ListMLE model: {:.4f}".format(listwise_model_result["ndcg_metric"]))

    #mspredictions = mse_model.predict(test, verbose=0)
    # sums = []
    # for index,prediction in enumerate(mspredictions):
    #     # print(prediction.argsort()[-10:])
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #     print(prediction[prediction.argsort()[-10:]])
    #     print(test['label'][index][prediction.argsort()[-10:]])
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #     sum = test['label'][index][prediction.argsort()[-5:]].sum()
    #     # print(sum)
    #     sums.append(sum)
    #
    # sums = np.array(sums)
    # # print(sums.shape)
    # print(sums.sum()/sums.shape[0])
    #
    # hgpredictions = hinge_model.predict(test, verbose=0)
    # sums = []
    # for index, prediction in enumerate(hgpredictions):
    #     # print(prediction.argsort()[-10:])
    #     # print(prediction[prediction.argsort()[-10:]])
    #     # print(test['label'][index][prediction.argsort()[-10:]])
    #     sum = test['label'][index][prediction.argsort()[-5:]].sum()
    #     # print(sum)
    #     sums.append(sum)
    #
    # sums = np.array(sums)
    # # print(sums.shape)
    # print(sums.sum() / sums.shape[0])

    lwpredictions = listwise_model.predict(test, verbose=0)
    sums = []
    for index, prediction in enumerate(lwpredictions):
        # print(prediction.argsort()[-10:])
        # print("==========================")
        # print(prediction[prediction.argsort()[-10:]])
        # print(test['label'][index][prediction.argsort()[-10:]])
        # print("==========================")
        sum = original_test[index][prediction.argsort()[-5:]].sum()
        # print(sum)
        sums.append(sum)

    sums = np.array(sums)
    # print(sums.shape)
    print(sums.sum() / sums.shape[0])
