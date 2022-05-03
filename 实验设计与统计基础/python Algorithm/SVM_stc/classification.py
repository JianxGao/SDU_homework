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


def accurate(pre, label):
    num = 0
    for i in range(len(pre)):
        if pre[i] != label[i]:
            num += 1
    return num


np.random.seed(1)
dataset = pd.read_csv('dataset_lll.csv').values
np.random.shuffle(dataset)
data, label = get_data_label(dataset)

mean = np.mean(data, axis=0)
std = np.std(data, axis=0)

data -= mean
data /= std

model = svm.SVC(kernel='linear', C=0.5)
model.fit(data, label)


# 提取参数
print(model.coef_.shape)
print(model.intercept_.shape)

b = model.intercept_
w = model.coef_
b = pd.DataFrame(b)
w = pd.DataFrame(w)
mean = pd.DataFrame(mean)
std = pd.DataFrame(std)
mean.to_csv('mean_normalise.csv')
std.to_csv('std_normalise.csv')
b.to_csv('bias_normalise.csv')
w.to_csv('weight_normalise.csv')
