import pickle

import numpy as np

from process_data import Process_data

train, test, original_test = Process_data.load_processed_data()
print("loading data")
loaded_model = pickle.load(open("listwise_model_55_days.pkl", "rb"))
print("predicting")

lwpredictions = loaded_model.predict(test, verbose=0)
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