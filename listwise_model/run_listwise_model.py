import tensorflow_ranking as tfr
from keras.callbacks import TensorBoard

from data_processor import DataProcessor
from listwise_model import ListwiseModel
import tensorflow as tf

if __name__ == "__main__":
    train = DataProcessor.load_rank_data()
    cached_train = train.batch(31).cache()
    tensorboard_callback = TensorBoard(log_dir="./logs")

    # for element in cached_train.take(1):
    #     print(f'Batch shape: {element["features"].shape}')
    #     batch_size = element["features"].shape[0]

    # Determine the length of your dataset
    data_length = tf.data.experimental.cardinality(train).numpy()

    # Split your data into a training and a validation set
    train_length = int(0.9 * data_length)  # 90% for training
    train_data = train.take(train_length).batch(31).cache()
    val_data = train.skip(train_length).batch(31).cache()  # remaining 10% for validation

    listwise_model = ListwiseModel(tfr.keras.losses.ListMLELoss())
    listwise_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    listwise_model.fit(train_data, epochs=10, verbose=2, callbacks=[tensorboard_callback], validation_data=val_data)

    # listwise_model_result = listwise_model.evaluate(cached_test, return_dict=True)
    # print("NDCG of the ListMLE model: {:.4f}".format(listwise_model_result["ndcg_metric"]))

    # Iterate over the batches of the validation data

    # Iterate over each batch
    for batch in val_data:
        # Unpack the features and labels
        features = batch["features"]
        labels = batch["labels"]

        # Convert to numpy for easier handling
        features_numpy, labels_numpy = features.numpy(), labels.numpy()

        # Iterate over each sample in the batch
        for i in range(len(features_numpy)):
            # Get individual feature and label
            individual_feature = features_numpy[i]
            individual_label = labels_numpy[i]
            # print(individual_feature)
            prediction = listwise_model.predict({"features":features_numpy[i]})
            print(prediction)
            print(individual_label)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # Do something with individual_feature and individual_label