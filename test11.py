import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimSun']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False
register_matplotlib_converters()
data = pd.read_excel('D:/作业/大三/数据挖掘/实验三/catering_sale.xls')
data = data.dropna()
# 月份转换
data['Year_Month'] = data['日期'].values.astype('datetime64[M]')
M_all_count = data.groupby('Year_Month')['销量'].sum()
result = data.describe()
# 中位数
result.loc['median'] = data.median()
# 极差
result.loc['range'] = result.loc['max'] - result.loc['min']
# 四分位距
var = result.loc['75%'] - result.loc['25%']
print(var/2)
print(result)

# 频数方图
plt.hist(M_all_count.values.tolist(), bins=M_all_count.index.strftime('%Y-%m').tolist())
plt.xlabel('月份')
plt.ylabel('销量')
plt.title('月度销售额的二维条形直方图')
plt.show()

# 按月份时间递增的销售额变化折线图(plot)
plt.plot(M_all_count.index.strftime('%Y-%m'), M_all_count.values)
plt.ylabel('销量')
plt.xlabel('日期')
plt.title('销售额变化折线图')
plt.show()
