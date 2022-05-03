import pandas as pd
import numpy as np
from sklearn import svm


def get_data_label(dataset):
    np.random.shuffle(dataset)
    data = []
    label = []
    for row in dataset:
        data.append(row[:-1])
        label.append(row[-1])
    return data, label


dataset = pd.read_csv('dataset_lll.csv').values
data, label = get_data_label(dataset)
total_num = dataset.shape[0]
k_fold = 5

test_num = int(total_num / k_fold)
np.random.seed(1)
for i in range(5):
    train_data = []
    test_data = []
    train_label = []
    test_label = []
    for index in range(len(data)):
        if i*test_num <= index < (i+1)*test_num:
            test_data.append(data[index])
            test_label.append(label[index])
        else:
            train_data.append(data[index])
            train_label.append(label[index])
    model = svm.SVC(kernel='linear', C=1)
    model.fit(data, label)
    y_pred = model.predict(test_data)
    # print(y_pred)
    b = model.intercept_
    w = model.coef_
    # k=0
    # for i in range(10):
    #     pred_xxx = np.dot(w[i], test_data[k])+b[i]
    #     print(pred_xxx, test_label[k])

    print(model.coef_.shape)
    print(model.intercept_.shape)

    num = 0

    for i in range(len(test_label)):
        if y_pred[i] != test_label[i]:
            num += 1
    print('wrong num:', num, ' test_num:', test_num)
    b = pd.DataFrame(b)
    w = pd.DataFrame(w)
    b.to_csv('bias.csv')
    w.to_csv('weight.csv')

