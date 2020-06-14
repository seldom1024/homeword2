import pandas as pd
from scipy.interpolate import lagrange


# s 为列向量， n为被插值的位置，k为取值前后的数据个数，默认5
def ploy_interp_column(s, n, k=5):
    # 取数
    y = s[list(range(n-k, n)) + list(range(n+1, n+1+k))]
    # 剔除空值
    y = y[y.notnull()]
    # 插入返回
    return lagrange(y.index, list(y))(n)


inputFile = "../doc/实验四/实验四使用数据/data/missing_data.xls"
outputFile = "../doc/实验四/实验四使用数据/data/missing_data_processed.xls"

data = pd.read_excel(inputFile, header=None)

# 逐行读取
for i in data.columns:
    for j in range(len(data)):
        # 判断为空
        if (data[i].isnull())[j]:
            data[i][j] = ploy_interp_column(data[i], j)

data.to_excel(outputFile, header=None, index=False)