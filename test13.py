import pandas as pd
import matplotlib.pyplot as plt
# 中文，小数处理
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# 可视化
def show(_data, _witch, _title):
    for j in range(0, _witch):
        plt.plot(data[_data == j], [j for i in _data[_data == j]], 'o')
    plt.ylim(-0.5, _witch - 0.5)
    plt.title(_title)
    plt.show()


witch = 6
w_list = [0.2 * i for i in range(witch)]
# 等宽离散 5等宽
data = pd.read_excel('D:/作业/大三/数据挖掘/实验三/discretization_data.xls')
data1 = pd.cut(data['肝气郁结证型系数'].values, witch, labels=range(witch))
show(data1, 5, "等宽离散化")


# 等频率离散化
w = data['肝气郁结证型系数'].describe(percentiles=w_list)[4:4 + witch + 1]
data3 = pd.cut(data['肝气郁结证型系数'], w, labels=range(witch))
show(data3, witch, "等频离散化")
