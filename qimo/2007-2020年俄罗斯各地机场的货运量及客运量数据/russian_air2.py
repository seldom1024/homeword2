import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    russian_CARGO_AND_PARCELS_file = "./russian_air_service_CARGO_AND_PARCELS.csv"
    russian_passenger_file = "./russian_passenger_air_service_2.csv"

    # cargo 处理
    cargo = pd.read_csv(russian_CARGO_AND_PARCELS_file)
    # 去掉空
    cargo = cargo.dropna()
    cargo.duplicated().nunique()
    cargo = cargo.drop_duplicates()
    # 计算
    d1 = cargo.groupby(["Year", "Airport name"])[cargo.columns.values.tolist()[2:-2]].sum()
    # 索引变成列名
    d1 = d1.reset_index()
    d1['总和'] = d1.apply(lambda x: x[cargo.columns.values.tolist()[2:-2]].sum(), axis=1)
    # 数据为0无意义
    d1 = d1[d1['总和'] > 0]
    d1 = d1.sort_values(["Airport name", "Year"]).reset_index().drop(["index"], axis=1)
    # 可视化
    for index in d1["Airport name"].unique():
        pd.DataFrame(d1[d1["Airport name"] == index].values.T, index=d1[d1["Airport name"] == index].columns,
                     columns=d1[d1["Airport name"] == index]["Year"]).iloc[2:-1].plot(kind='line')
        plt.show()

    # passenger 处理
    passenger = pd.read_csv(russian_passenger_file)
    # 去掉空
    passenger = passenger.dropna()
    passenger.duplicated().nunique()
    passenger = passenger.drop_duplicates()
    # 计算
    d1 = passenger.groupby(["Year", "Airport name"])[passenger.columns.values.tolist()[2:-2]].sum()
    # 索引变成列名
    d1 = d1.reset_index()
    d1['总和'] = d1.apply(lambda x: x[cargo.columns.values.tolist()[2:-2]].sum(), axis=1)
    # 数据为0无意义
    d1 = d1[d1['总和'] > 0]
    d1 = d1.sort_values(["Airport name", "Year"]).reset_index().drop(["index"], axis=1)
    # 可视化
    for index in d1["Airport name"].unique():
        pd.DataFrame(d1[d1["Airport name"] == index].values.T, index=d1[d1["Airport name"] == index].columns,
                     columns=d1[d1["Airport name"] == index]["Year"]).iloc[2:-1].plot(kind='line')
        plt.show()
