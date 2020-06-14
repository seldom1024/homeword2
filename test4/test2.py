import pandas as pd
from random import shuffle
# from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, roc_curve  # 导入混淆矩阵函数、roc曲线
import matplotlib.pyplot as plt  # 导入作图库
import joblib
import numpy as np


def cm_plot(y, yp):
    # 混淆矩阵
    cm = confusion_matrix(y, yp)
    plt.matshow(cm, cmap=plt.cm.Greens)  # 画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
    plt.colorbar()  # 颜色标签
    for x in range(len(cm)):  # 数据标签
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
    plt.ylabel('True label')  # 坐标轴标签
    plt.xlabel('Predicted label')  # 坐标轴标签
    return plt


# 数据划分
dataFile = "../doc/实验四/实验四使用数据/data/model.xls"
data = pd.read_excel(dataFile)
# 转成矩阵
data = data.as_matrix()
# 打乱
shuffle(data)
p = 0.8
train = data[:int(len(data) * p), :]
test = data[int(len(data) * p):, :]

# 构建 CART 决策树
treeFile = "../doc/实验四/实验四使用数据/data/tree.pkl"
tree = DecisionTreeClassifier()
tree.fit(train[:, :3], train[:, 3])
# 保存模型
joblib.dump(tree, treeFile)
# 可视化
cm_plot(train[:, 3], tree.predict(train[:, :3])).show()


# K近邻算法
def calc_distance(a, b):
    # 对应元素相减
    temp = np.subtract(a, b)
    # 元素分别平方
    temp = np.power(temp, 2)
    # 先求和再开方
    distance = np.sqrt(temp.sum())
    return distance


dis = []
for i in range(len(test)):
    dis.append(calc_distance(train[i], test))
kTest = np.column_stack((test, dis))
k = int(len(test)*0.5)
kTest = kTest[:k]
cm_plot(kTest[:, 3], tree.predict(kTest[:, :3])).show()


# 绘制决策树模型的roc曲线
fpr, tpr, thresholds = roc_curve(test[:, 3],
                                 tree.predict_proba(test[:, :3])[:, 1],
                                 pos_label=1)
plt.plot(fpr, tpr, label="ROC of CART")
plt.ylim(0, 1.05)
plt.xlim(0, 1.05)
plt.show()


fpr, tpr, thresholds = roc_curve(kTest[:, 3],
                                 tree.predict_proba(kTest[:, :3])[:, 1],
                                 pos_label=1)
plt.plot(fpr, tpr, label="ROC of K")
plt.ylim(0, 1.05)
plt.xlim(0, 1.05)
plt.show()

