import tensorflow as tf
from pair_wise_model import StockMovementPredictionModel
from pair_wise_linear_model import PairwiseRankingModel
from data_processor import Data_processor
import numpy as np
from tensorflow.keras.callbacks import TensorBoard
import pickle


if __name__ == "__main__":
    # StockData.getAllPriceData()
    # StockData.cutTimeCSV()
    # StockData.updatePriceChange()
    #StockData.combinePriceData(2513)

    process_data = Data_processor()
    inputs1,inputs2, labels = process_data.load_processed_data()
    # train,test, original_test = process_data.fetch_data()
    tensorboard_callback = TensorBoard(log_dir="./logs")
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  # The metric to monitor
        patience=3,  # Number of epochs with no improvement to wait
        mode='min'  # Training will stop when the quantity monitored has stopped decreasing
    )
    # Create the model
    model = StockMovementPredictionModel()

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy')

    inputs1 = np.array(inputs1)
    inputs2 = np.array(inputs2)
    labels = np.array(labels)
    inputs1 = inputs1.astype('float32')
    inputs2 = inputs2.astype('float32')
    labels = labels.astype('float32')

    print(inputs1.shape)
    print(inputs2.shape)
    print(labels.shape)

    # Fit the model
    model.fit([inputs1, inputs2], labels, epochs=1000, batch_size=256, verbose=2,
              callbacks=[tensorboard_callback],
              validation_split=0.1)
    model.save("pairwise_5_symbols_model")

