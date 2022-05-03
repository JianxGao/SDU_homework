import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from IPython.display import Image
import pydotplus
import numpy as np


np.random.seed(1)
dataset = pd.read_csv('dataset_lll.csv').values
np.random.shuffle(dataset)
data, label = dataset[:, :-1], dataset[:, -1]
# 训练模型，限制树的最大深度4
clf = RandomForestClassifier(max_depth=4, n_estimators=10)
# 拟合模型
clf.fit(data, label)

Estimators = clf.estimators_
for index, model in enumerate(Estimators):
    filename = 'Random_Forest_' + str(index) + '.pdf'
    dot_data = tree.export_graphviz(model, out_file=None,
                                    # feature_names=iris.feature_names,
                                    # class_names=iris.target_names,
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)
    Image(graph.create_png())
    graph.write_pdf(filename)


