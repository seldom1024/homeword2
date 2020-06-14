from sklearn.decomposition import PCA
import pandas as pd


# 参数初始化
inputFile = 'D:/作业/大三/数据挖掘/实验三/principal_component.xls'
outputFile = './dimention_reducted.xls'  # 降维后的数据

data = pd.read_excel(inputFile)  # 读入数据
pca = PCA()  # 保留所有成分
pca.fit(data)
# print(pca.components_)  # 返回模型的各个特征向量
# 返回各个成分各自的方差百分比(也称贡献率）
print(pca.explained_variance_ratio_.max())
# 选取累计贡献率大于80%的主成分（3个主成分）
pca = PCA(3)
pca.fit(data)
# 降低维度
low_d = pca.transform(data)
pd.DataFrame(low_d).to_excel(outputFile)