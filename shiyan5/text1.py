import pandas as pd
# 读入数据
data = pd.read_excel("./zscoredata.xls")
# 标准化
data = (data - data.mean(axis=0)) / (data.std(axis=0))
data.columns = ['S' + i for i in data.columns]
# 保存数据
data.to_excel("./standardization.xls", index=False)
