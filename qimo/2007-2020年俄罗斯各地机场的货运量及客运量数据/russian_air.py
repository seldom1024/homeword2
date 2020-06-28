import pandas as pd
import matplotlib.pyplot as plt
# 导入线性回归方程和模型选择方法
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import SelectFromModel


# 可视化功能
def plt_show(data, title):
    for index in data["Airport name"].unique():
        pd.DataFrame(data[data["Airport name"] == index].values.T, index=data[data["Airport name"] == index].columns,
                     columns=data[data["Airport name"] == index]["Year"]).iloc[2:-1].plot(kind='line',
                                                                                          title=title + "_" + index,
                                                                                          figsize=(5, 5))
        plt.show()


# 根据Airport name 跟 year 维度统计
def data_handle(date, title):
    # 数据清洗
    date = date.dropna()
    date.duplicated().nunique()
    date = date.drop_duplicates()
    data_h = date.groupby(["Year", "Airport name"])[date.columns.values.tolist()[2:-2]].sum()
    # 索引变成列名
    data_h = data_h.reset_index()
    data_h['Col_sum'] = data_h.apply(lambda x: x[date.columns.values.tolist()[2:-2]].sum(), axis=1)
    # 数据为0无意义
    data_h = data_h[data_h['Col_sum'] > 0]
    data_h = data_h.sort_values(["Airport name", "Year"]).reset_index().drop(["index"], axis=1)
    plt_show(data_h, title)


# Year 的维度统计
def date_handle_all(data, title):
    all_date = data.groupby(["Year"])[data.columns.values.tolist()[2:-2]].sum()
    pd.DataFrame(all_date.values.T, index=all_date.columns, columns=all_date.index).plot(kind='line', title=title)
    plt.show()


# 数据路径
russian_CARGO_AND_PARCELS_file = "./russian_air_service_CARGO_AND_PARCELS.csv"
russian_passenger_file = "./russian_passenger_air_service_2.csv"
# 数据读取
cargo_date = pd.read_csv(russian_CARGO_AND_PARCELS_file)
passenger_date = pd.read_csv(russian_passenger_file)

if __name__ == '__main__':
    data_handle(cargo_date, "cargo")
    data_handle(passenger_date, "passenger")
    date_handle_all(passenger_date, "passenger_year")
    date_handle_all(cargo_date, "cargo_year")
    print("end")

    # https://blog.csdn.net/qq_36327687/article/details/85010666
    # 自变量特征
    feature = data[['月份', '季度', '广告费用', '客流量']]
    # 建立线性回归模型
    LrModel = LinearRegression()
    # 建立选择回归模型
    selectFromModel = SelectFromModel(LrModel)
    # fit方法训练选择，自动选择最优的特征数
    selectFromModel.fit_transform(
        feature,
        data['销售额']
    )
