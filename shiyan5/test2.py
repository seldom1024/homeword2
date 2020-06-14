from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd


def photo_handle(handle_file):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    p = handle_file.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
    [p[i].set_ylabel('密度') for i in range(5)]
    plt.legend()
    return plt


data = pd.read_excel("./preprocesseddata.xls")
file = data.iloc[:, -5:21]  # 截取最后5列数据

kMeans = KMeans(n_clusters=5, n_jobs=4, max_iter=500, random_state=1234).fit(file)  # 3个类别聚类最大循环次数500,开始聚类
count = pd.Series(kMeans.labels_).value_counts()  # 统计数目
center = pd.DataFrame(kMeans.cluster_centers_)  # 找出聚类中心
r = pd.concat([center, count], axis=1)  # 横向连接
r.columns = list(file.columns) + ['类别数目']
r = pd.concat([file, pd.Series(kMeans.labels_, index=file.index)], axis=1)
r.columns = list(file.columns) + ['聚类类别']

for i in range(5):
    photo_handle(file[r["聚类类别"] == i]).show()


