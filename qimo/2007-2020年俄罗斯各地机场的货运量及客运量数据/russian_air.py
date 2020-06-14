import pandas as pd
import matplotlib.pyplot as plt


def plt_show(data, title):
    for index in data["Airport name"].unique():
        pd.DataFrame(data[data["Airport name"] == index].values.T, index=data[data["Airport name"] == index].columns,
                     columns=data[data["Airport name"] == index]["Year"]).iloc[2:-1].plot(kind='line',
                                                                                          title=title + "_" + index,
                                                                                          figsize=(5, 5))
        plt.show()


def data_handle(date, title):
    date = date.dropna()
    date.duplicated().nunique()
    date = date.drop_duplicates()
    data_h = date.groupby(["Year", "Airport name"])[date.columns.values.tolist()[2:-2]].sum()
    data_h = data_h.reset_index()  # 索引变成列名
    data_h['Col_sum'] = data_h.apply(lambda x: x[date.columns.values.tolist()[2:-2]].sum(), axis=1)
    data_h = data_h[data_h['Col_sum'] > 0]  # 数据为0无意义
    data_h = data_h.sort_values(["Airport name", "Year"]).reset_index().drop(["index"], axis=1)
    plt_show(data_h, title)


def date_handle_all(data, title):
    all_date = data.groupby(["Year"])[data.columns.values.tolist()[2:-2]].sum()
    pd.DataFrame(all_date.values.T, index=all_date.columns, columns=all_date.index).plot(kind='line', title=title)
    plt.show()


russian_CARGO_AND_PARCELS_file = "./russian_air_service_CARGO_AND_PARCELS.csv"
russian_passenger_file = "./russian_passenger_air_service_2.csv"

cargo_date = pd.read_csv(russian_CARGO_AND_PARCELS_file)
passenger_date = pd.read_csv(russian_passenger_file)

# cargo
# 数据清洗（去除空值、重复项、异常项）
# cargo_date = cargo_date.dropna()
# cargo_date.duplicated().nunique()
# cargo_date = cargo_date.drop_duplicates()
#
# data1 = cargo_date.groupby(["Year", "Airport name"])[cargo_date.columns.values.tolist()[2:-2]].sum()
# da = data1.reset_index()  # 索引变成列名
#
# da['Col_sum'] = da.apply(lambda x: x[cargo_date.columns.values.tolist()[2:-2]].sum(), axis=1)
# da = da[da['Col_sum'] > 0]  # 数据为0无意义
# da = da.sort_values(["Airport name", "Year"]).reset_index().drop(["index"], axis=1)

if __name__ == '__main__':
    data_handle(cargo_date, "cargo")
    data_handle(passenger_date, "passenger")
    date_handle_all(passenger_date, "passenger_year")
    date_handle_all(cargo_date, "cargo_year")
    print("end")
