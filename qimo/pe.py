import pandas as pd
import numpy as np
import pyecharts.options as opts
import pyecharts as pe

# 设置pandas参数，显示等
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('expand_frame_repr', False)  # 省略显示

# 数据导入
data = pd.read_csv("./Online_Retail.csv")

# 查看导入情况
# print(data.head(10))
# print(data.info())
# print(data.dtypes)

# 数据清洗（去除空值、重复项、异常项）
data = data.dropna()
# 查看是否有重复数据，去掉重复数据
data.duplicated().nunique()
data = data.drop_duplicates()
# 含有？的数据处理
data = data[~data['Description'].str.contains('？')]  # 删除某列包含特殊字符的行
# 价格负数
data = data[data['UnitPrice'] > 0]
# 查看清洗后的数据
# print(data.info())


# 数据转换
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data['CustomerID'] = data['CustomerID'].astype('int').astype('object')
# data.info()
# print(data.head(1))
# print(data.dtypes)#类型查看
# print(data.head().to_html)#格式输出
# data.head(10)#jupyter上运行（表格对齐）


# 时间提取
data['Hour'] = data['InvoiceDate'].dt.hour
data['Day'] = data['InvoiceDate'].dt.day
data['Dayofweek'] = data['InvoiceDate'].dt.dayofweek
data['Weekofyear'] = data['InvoiceDate'].dt.weekofyear
data['Year_Month'] = data['InvoiceDate'].values.astype('datetime64[M]')  # D日精度，M月精度，Y年精度，周进度（计算时候切换）
data['Year_Month_Week'] = data['InvoiceDate'].values.astype('datetime64[W]')
data['Year_Month_Day'] = data['InvoiceDate'].values.astype('datetime64[D]')

# 每次交易的总价
data['Toa_Pri'] = data['Quantity'] * data['UnitPrice']
# 销售总
M_count = data.groupby('Year_Month')['Toa_Pri'].sum()
# 销售金额计算退款
M_all_count = data[data['Quantity'] > 0].groupby('Year_Month')['Toa_Pri'].sum()

# 每月销售情况
M_count_tu = (
    pe.charts.Line()
        .add_xaxis(M_count.index.strftime('%Y-%m').tolist())
        .add_yaxis('销售成交总额', M_count.values.tolist(), is_smooth=False, is_selected=False, is_symbol_show=False)
        .add_yaxis('销售总额(除去退款)', M_all_count.values.tolist(), is_smooth=False, is_selected=False, is_symbol_show=False)
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ), ),
                         title_opts=opts.TitleOpts(title="金额"),
                         tooltip_opts=opts.TooltipOpts(trigger="axis"),
                         toolbox_opts=opts.ToolboxOpts(), )
)
M_count_tu.render_notebook()

# 每个国家avg
Country_Avg = data.groupby('Country')['Toa_Pri'].sum() / data.groupby('Country')['Country'].count()
Country_Avg_tu = (
    pe.charts.Funnel()
        .add("平均金额", [list(z) for z in zip(Country_Avg.index.tolist(), Country_Avg.values.tolist())])
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="国家客户订单平均金额"),
        toolbox_opts=opts.ToolboxOpts(),
        # init_opts = opts.InitOpts(height = "900px"),
        legend_opts=opts.LegendOpts(is_show=False))
)
Country_Avg_tu.render_notebook()

# 消费次数跟金额关系
Cus_buy_times_all = data[data['Quantity'] > 0].groupby('CustomerID')['InvoiceNo'].nunique()  # 每个客户消费次数(一个时间算一次)
Cus_buy_times_df = data[data['Quantity'] > 0].groupby(['CustomerID', 'Description'])[
    'InvoiceNo'].nunique()  # nunique()#每个客户消费不同产品的次数
Cus_buy_money_all = data[data['Quantity'] > 0].groupby('CustomerID')['Toa_Pri'].sum()  # 每个客户消费总金额
Cus_buy_money_df = data[data['Quantity'] > 0].groupby(['CustomerID', 'InvoiceNo'])['Toa_Pri'].sum()  # 每个客户消费不同产品总金额
t1 = Cus_buy_times_df.reset_index(name='Buy_times_df')  # reset_index()将所有索引级别转换为列，并用简单的RangeIndex作为新的索引,取名为 Buy_times
t2 = Cus_buy_money_df.reset_index(name='Buy_money_df')
t3 = Cus_buy_times_all.reset_index(name='Buy_times_all')  # reset_index()将所有索引级别转换为列，并用简单的RangeIndex作为新的索引,取名为 Buy_times
t4 = Cus_buy_money_all.reset_index(name='Buy_money_all')
t2.insert(2, 'Buy_times_df', t1.Buy_times_df)  # 插入数据
t4.insert(2, 'Buy_times_all', t3.Buy_times_all)  # 插入数据
Buy_times_mon_all = t4
Buy_times_mon_df = t2
# 消费次数跟金额关系（单个产品）
k2 = Buy_times_mon_df.Buy_money_df.values.tolist()
k1 = Buy_times_mon_df.Buy_times_df.values.tolist()
z = list(zip(k1, k2))  # 转化二元组
Buy_times_mon_df_tu = (
    pe.charts.Polar()
        .add("", z, type_="scatter", label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="消费次数跟金额关系(单个产品)"),
                         toolbox_opts=opts.ToolboxOpts(), )
)
Buy_times_mon_df_tu.render_notebook()
# 消费次数跟金额关系(交易总)
k2 = Buy_times_mon_all.Buy_money_all.values.tolist()
k1 = Buy_times_mon_all.Buy_times_all.values.tolist()
z = list(zip(k1, k2))  # 转化二元组
Buy_times_mon_all_tu = (
    pe.charts.Polar()
        .add("", z, type_="scatter", label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ),
                         ),
                         title_opts=opts.TitleOpts(title="消费次数跟金额关系(交易总)"),
                         toolbox_opts=opts.ToolboxOpts(), )
)
Buy_times_mon_all_tu.render_notebook()

# 复购率
# 复购率月
Back_buy_count_m = data[data['Quantity'] > 0].pivot_table(index=['CustomerID'],
                                                          columns=['Year_Month'],
                                                          values='InvoiceNo',
                                                          aggfunc='nunique').fillna(
    0)  # count 表示计算每次购买的产品数，nunique 表示购买次数
# Back_buy_count_m.columns = Back_buy_count_m.columns.astype('str')
# 如果在一个月之内再来购买就是x>=1表示一个月的购买次数
Back_buy_count_m = Back_buy_count_m.applymap(lambda x: 1 if x > 1 else 0)
Back_buy_count_m = (Back_buy_count_m.sum() / Back_buy_count_m.count())
lis_tra_m = Back_buy_count_m.reset_index(name='Back_buy_count_m')

# 复购率周
Back_buy_count_w = data[data['Quantity'] > 0].pivot_table(index=['CustomerID'],
                                                          columns=['Year_Month', 'Year_Month_Week'],
                                                          values='InvoiceNo',
                                                          aggfunc='nunique').fillna(
    0)  # count 表示计算每次购买的产品数，nunique 表示购买次数
# 如果在一个月之内再来购买就是x>=1表示一个月的购买次数
Back_buy_count_w = Back_buy_count_w.applymap(lambda x: 1 if x > 1 else 0)
Back_buy_count_w = (Back_buy_count_w.sum() / Back_buy_count_w.count())

# list  = Back_buy_count_w['2010-12-01'].values#values 表示取值组成数组
# 转化表格
lis_tra = Back_buy_count_w.reset_index(name='Back_buy_count_w')
lis_m = lis_tra['Year_Month'].unique()  # 提取月信息

# 数据集（一个月的周复购率）
lis_tu_data = np.array([None, None, None, None, None, None])
for i in lis_m:
    temp = Back_buy_count_w[i].values
    while (len(temp) != 6):
        temp = np.append(temp, None)
    lis_tu_data = np.row_stack((lis_tu_data, temp))
# 去除第0行 ，*100，美观，百分率
lis_tu_data = np.delete(lis_tu_data, 0, axis=0).astype(np.float) * 100
lis_tu_data = lis_tu_data.tolist()

# 数据处理
mylist_inser = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
for i in range(13):
    for j in range(5):
        if np.isnan(lis_tu_data[i][j + 1]):
            mylist_inser[i] = lis_tu_data[i][j]
            break
        elif j == 4:
            mylist_inser[i] = lis_tu_data[i][j + 1]
            break
# 出入一列数据
lis_tu_data = np.insert(lis_tu_data, 1, values=mylist_inser, axis=1).tolist()


# 周k图
def kline_base() -> pe.charts.Kline:
    K = (
        pe.charts.Kline()
            .add_xaxis(
            ["2010/12", "2011/1", "2011/2", "2011/3", "2011/4", "2011/5", "2011/6", "2011/7", "2011/8", "2011/9",
             "2011/10", "2011/11", "2011/12"])
            .add_yaxis("周复购率月K图", lis_tu_data,
                       markline_opts=opts.MarkLineOpts(
                           data=[opts.MarkLineItem(type_="max", value_dim="close")]
                       ), )
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_scale=True),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title="K图"),
        )
    )
    line = (
        pe.charts.Line()
            .add_xaxis(
            ["2010/12", "2011/1", "2011/2", "2011/3", "2011/4", "2011/5", "2011/6", "2011/7", "2011/8", "2011/9",
             "2011/10", "2011/11", "2011/12"])
            .add_yaxis("月复购率年变化", [x * 100 for x in lis_tra_m['Back_buy_count_m'].tolist()],
                       is_selected=False,
                       is_symbol_show=False)
    )
    K.overlap(line)
    return K


Back_buy_count_wm_Ktu = kline_base().set_global_opts(
    yaxis_opts=opts.AxisOpts(is_scale=True, splitarea_opts=opts.SplitAreaOpts(
        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
    ), ),
    xaxis_opts=opts.AxisOpts(is_scale=True),
    datazoom_opts=[opts.DataZoomOpts()],  # 时间选择
    title_opts=opts.TitleOpts(title="复购率图(%)"),
    toolbox_opts=opts.ToolboxOpts(),
)
Back_buy_count_wm_Ktu.render_notebook()

# 客单价
Buy_count_p = data[data['Quantity'] > 0].groupby('Year_Month')['CustomerID'].nunique()  # 每月消费人数
# 每天客单价
Customer_ev_d = data[data['Quantity'] > 0].groupby('Year_Month_Day')['Toa_Pri'].sum() / \
                data[data['Quantity'] > 0].groupby('Year_Month_Day')['InvoiceDate'].nunique()
# 每周客单价
Customer_ev_w = data[data['Quantity'] > 0].groupby('Year_Month_Week')['Toa_Pri'].sum() / \
                data[data['Quantity'] > 0].groupby('Year_Month_Week')['InvoiceDate'].nunique()
# 每月客单价
Customer_ev_m = data[data['Quantity'] > 0].groupby('Year_Month')['Toa_Pri'].sum() / \
                data[data['Quantity'] > 0].groupby('Year_Month')['InvoiceDate'].nunique()
Customer_ev_d_tu = (
    pe.charts.Line()
        .add_xaxis(Customer_ev_d.index.strftime('%Y-%m-%d').tolist())
        .add_yaxis('每日客单价',
                   Customer_ev_d.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="日客单价均值")]),
                   )
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ), title_opts=opts.TitleOpts(title="每日客单价(年变化)"),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        toolbox_opts=opts.ToolboxOpts(),
        datazoom_opts=[opts.DataZoomOpts()],  # 时间选择
        tooltip_opts=opts.TooltipOpts(trigger="axis"))
)
Customer_ev_d_tu.render_notebook()

Customer_ev_w_tu = (
    pe.charts.Line()
        .add_xaxis(Customer_ev_w.index.strftime('%Y-%m-%d').tolist())
        .add_yaxis('每周客单价',
                   Customer_ev_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="周客单价均值")]),
                   )
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="每周客单价(年变化)"),
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        datazoom_opts=[opts.DataZoomOpts()],  # 时间选择
        tooltip_opts=opts.TooltipOpts(trigger="axis"))
)
Customer_ev_w_tu.render_notebook()

Customer_ev_m_tu = (
    pe.charts.Line()
        .add_xaxis(Customer_ev_m.index.strftime('%Y-%m-%d').tolist())
        .add_yaxis('每月客单价',
                   Customer_ev_m.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   # color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="月客单价均值")]),
                   )
        .add_yaxis('每月客数量',
                   Buy_count_p.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   # color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="月客数量均值")]),
                   )
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="每月客单价&数量"),
        toolbox_opts=opts.ToolboxOpts(),
        tooltip_opts=opts.TooltipOpts(trigger="axis"))
)
Customer_ev_m_tu.render_notebook()

# 消费国家情况
# 订单数量
Country_pro_sum = data[data['Quantity'] > 0].groupby('Country')['InvoiceNo'].nunique().sort_values()
# 消费金额
Country_money_sum = data[data['Quantity'] > 0].groupby('Country')['Toa_Pri'].sum().sort_values()
# 客户数量
Country_customer_sum = data[data['Quantity'] > 0].groupby('Country')['CustomerID'].nunique().sort_values()
# 图表示
Country_tu_sum = (
    pe.charts.Bar()
        .add_xaxis(Country_pro_sum.index.tolist())
        .add_yaxis("订单数量",
                   Country_pro_sum.values.tolist(),
                   is_selected=False,
                   )
        .add_yaxis("消费金额",
                   [int(x) for x in Country_money_sum.values.tolist()],
                   is_selected=False,
                   )
        .add_yaxis("客户数量",
                   Country_customer_sum.values.tolist(),
                   is_selected=False,
                   )
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ),
                         ),
                         title_opts=opts.TitleOpts(title="消费国家情况"),
                         toolbox_opts=opts.ToolboxOpts(),
                         datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                         )
)
Country_tu_sum.render_notebook()

# 交易情况（次数&金额）
# 日
Sell_count_d = data[data['Quantity'] > 0].groupby('Year_Month_Day')['CustomerID'].nunique()
Sell_money_d = data[data['Quantity'] > 0].groupby('Year_Month_Day')['Toa_Pri'].sum()
Sell_money_d_re = data.groupby('Year_Month_Day')['Toa_Pri'].sum()  # 销售（减去退款）
# 周
Sell_count_w = data[data['Quantity'] > 0].groupby('Year_Month_Week')['CustomerID'].nunique()
Sell_money_w = data[data['Quantity'] > 0].groupby('Year_Month_Week')['Toa_Pri'].sum()
Sell_money_w_re = data.groupby('Year_Month_Week')['Toa_Pri'].sum()  # 销售（减去退款）
# 月
Sell_count_m = data[data['Quantity'] > 0].groupby('Year_Month')['CustomerID'].nunique()
Sell_money_m = data[data['Quantity'] > 0].groupby('Year_Month')['Toa_Pri'].sum()
Sell_money_m_re = data.groupby('Year_Month')['Toa_Pri'].sum()  # 销售（减去退款）
# 图
Sell_d_tu = (
    pe.charts.Line()
        .add_xaxis(Sell_count_d.index.strftime('%Y-%m-%d').tolist())
        .add_yaxis('日交易数量',
                   Sell_count_d.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="日交易数量均值")]),
                   )
        .add_yaxis('日交易金额',
                   Sell_money_d.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="日交易金额均值")]),
                   )
        .add_yaxis('日销售金额(减去退款)',
                   Sell_money_d_re.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="日销售金额均值")]),
                   )
        .add_yaxis('每日客单价',
                   Customer_ev_d.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   # color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="日客单价均值")]),
                   )
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="日交易情况(年变化)"),
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        datazoom_opts=[opts.DataZoomOpts()],  # 时间选择
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        legend_opts=opts.LegendOpts(type_='scroll', pos_top='5%'))
)
Sell_d_tu.render_notebook()

Sell_w_tu = (
    pe.charts.Line()
        .add_xaxis(Sell_count_w.index.strftime('%Y-%m-%d').tolist())
        .add_yaxis('周交易数量',
                   Sell_count_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="周交易数量均值")]),
                   )
        .add_yaxis('周交易金额',
                   Sell_money_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="周交易金额均值")]),
                   )
        .add_yaxis('周销售金额(减去退款)',
                   Sell_money_w_re.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="周销售金额均值")]),
                   )
        .add_yaxis('每周客单价',
                   Customer_ev_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   # color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="周客单价均值")]),
                   )
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="周交易情况(年变化)"),
        toolbox_opts=opts.ToolboxOpts(),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        datazoom_opts=[opts.DataZoomOpts()],  # 时间选择
        legend_opts=opts.LegendOpts(type_='scroll', pos_top='5%'))
)
Sell_w_tu.render_notebook()

Sell_m_tu = (
    pe.charts.Line()
        .add_xaxis(Sell_count_m.index.strftime('%Y-%m').tolist())
        .add_yaxis('月交易数量',
                   Sell_count_m.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="月交易数量均值")]),
                   )
        .add_yaxis('月交易金额',
                   Sell_money_m.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="月交易金额均值")]),
                   )
        .add_yaxis('月销售金额(减去退款)',
                   Sell_money_m_re.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="月销售金额均值")]),
                   )
        .add_yaxis('每月客单价',
                   Customer_ev_m.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   # color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="月客单价均值")]),
                   )
        .add_yaxis('每月客数量',
                   Buy_count_p.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   # color='rgb(0,0,255)',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="月客数量均值")]),
                   )
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="月交易情况(年变化)"),
        toolbox_opts=opts.ToolboxOpts(),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        legend_opts=opts.LegendOpts(type_='scroll', pos_top='5%'))
)
Sell_m_tu.render_notebook()

# 购买时间行为
# 日内
Buy_time_count_d = data[data['Quantity'] > 0].groupby('Hour')['InvoiceNo'].nunique()
Buy_time_money_d = data[data['Quantity'] > 0].groupby('Hour')['Toa_Pri'].sum()
# 周内
Buy_time_count_w = data[data['Quantity'] > 0].groupby('Dayofweek')['InvoiceNo'].nunique()
Buy_time_money_w = data[data['Quantity'] > 0].groupby('Dayofweek')['Toa_Pri'].sum()
Buy_time_count_bw = data[data['Quantity'] < 0].groupby('Dayofweek')['InvoiceNo'].nunique()
Buy_time_money_bw = data[data['Quantity'] < 0].groupby('Dayofweek')['Toa_Pri'].sum().abs()

# 完成

# 周&时
Buy_time_count_wd = data[data['Quantity'] > 0].groupby(['Dayofweek', 'Hour'])['InvoiceNo'].nunique()
Buy_time_money_wd = data[data['Quantity'] > 0].groupby(['Dayofweek', 'Hour'])['Toa_Pri'].sum()
# 浮点数处理
# lis_tra_cwd = np.array(Buy_time_count_wd.reset_index(name = 'Buy_time_count_wd')).tolist()
Buy_time_count_wd = Buy_time_count_wd.reset_index(name='Buy_time_count_wd')
# Buy_time_count_wd['Buy_time_count_wd'] = Buy_time_count_wd['Buy_time_count_wd'].astype('int')
lis_tra_mwdc = np.array(Buy_time_count_wd)
lis_tra_mwdc = np.array(lis_tra_mwdc)
array11 = lis_tra_mwdc[:, 0].reshape(73, 1)
array21 = (lis_tra_mwdc[:, 1] - 6).reshape(73, 1)
array31 = lis_tra_mwdc[:, 2].astype(int).reshape(73, 1)
array345 = np.hstack((array21, array11, array31)).tolist()

Buy_time_money_wd = Buy_time_money_wd.reset_index(name='Buy_time_count_wd')
Buy_time_money_wd['Buy_time_count_wd'] = Buy_time_money_wd['Buy_time_count_wd'].astype('int')
lis_tra_mwd = np.array(Buy_time_money_wd)
lis_tra_mwd = np.array(lis_tra_mwd)
array1 = lis_tra_mwd[:, 0].reshape(73, 1)
array2 = (lis_tra_mwd[:, 1] - 6).reshape(73, 1)
array3 = (lis_tra_mwd[:, 2] / 1000).astype(int).reshape(73, 1)
array34 = np.hstack((array2, array1, array3)).tolist()
# 图
Week_day_tu = (
    pe.charts.HeatMap()
        .add_xaxis([str(x) + '时' for x in Buy_time_count_d.index.tolist()])
        .add_yaxis("销售额", ["周一", "周二", "周三", "周四", "周五", "周六", "周日"], array34, is_selected=False, )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="销售额(小时&星期的关系)"),
        visualmap_opts=opts.VisualMapOpts(),
    )
        .add_yaxis("销售量", ["周一", "周二", "周三", "周四", "周五", "周六", "周日"], array345, is_selected=False, )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="销售额(小时&星期的关系)"),
        toolbox_opts=opts.ToolboxOpts(),
        visualmap_opts=opts.VisualMapOpts(range_text=['多', '少']),
    )
)
Week_day_tu.render()
# 完成


# 图
Buy_time_count_wtu = (
    pe.charts.Line()
        .add_xaxis(["周一", "周二", "周三", "周四", "周五", "周末"])
        .add_yaxis('交易次数',
                   Buy_time_count_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False
                   )
        .add_yaxis('交易金额',
                   Buy_time_money_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False
                   )
        .add_yaxis('退款金额',
                   Buy_time_money_bw.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False
                   )
        .add_yaxis('退款订单数',
                   Buy_time_count_bw.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False
                   )
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="一周内交易统计(交易次数&金额)"),
        toolbox_opts=opts.ToolboxOpts(),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        legend_opts=opts.LegendOpts(type_='scroll', pos_top='5%'))
)
Buy_time_count_wtu.render_notebook()

Buy_time_count_dtu = (
    pe.charts.Line()
        .add_xaxis([str(x) for x in Buy_time_count_d.index.tolist()])
        .add_yaxis('交易次数',
                   Buy_time_count_d.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False
                   )
        .add_yaxis('交易金额',
                   Buy_time_money_d.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False
                   )
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ),
                         ),
                         title_opts=opts.TitleOpts(title="一日内交易统计(交易次数&金额)"),
                         toolbox_opts=opts.ToolboxOpts(),
                         tooltip_opts=opts.TooltipOpts(trigger="axis"),
                         legend_opts=opts.LegendOpts(type_='scroll', pos_top='5%'))
)
Buy_time_count_dtu.render_notebook()

# 退款情况
Ret_count_w = data[data['Quantity'] < 0].groupby('Year_Month_Week')['InvoiceNo'].nunique()
Ret_count_m = data[data['Quantity'] < 0].groupby('Year_Month')['InvoiceNo'].nunique()
Ret_money_w = data[data['Quantity'] < 0].groupby('Year_Month_Week')['Toa_Pri'].sum().abs()
Ret_money_m = data[data['Quantity'] < 0].groupby('Year_Month')['Toa_Pri'].sum().abs()
Ret_rate_w = data[data['Quantity'] < 0].groupby('Year_Month_Week')['InvoiceNo'].nunique() / \
             data[data['Quantity'] > 0].groupby('Year_Month_Week')['InvoiceNo'].nunique()
Ret_rate_m = data[data['Quantity'] < 0].groupby('Year_Month')['InvoiceNo'].nunique() / \
             data[data['Quantity'] > 0].groupby('Year_Month')['InvoiceNo'].nunique()
# 图
Ret_w_tu = (
    pe.charts.Line()
        .add_xaxis(Ret_count_w.index.strftime('%Y-%m-%d').tolist())
        .add_yaxis('周退款数量',
                   Ret_count_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   )
        .add_yaxis('周退款率',
                   Ret_rate_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   )
        .add_yaxis('周退款金额',
                   Ret_money_w.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   )
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        title_opts=opts.TitleOpts(title="周退款情况(年变化)"),
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        datazoom_opts=[opts.DataZoomOpts()],  # 时间选择
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        legend_opts=opts.LegendOpts(type_='scroll', pos_top='5%'))
)
Ret_w_tu.render_notebook()

Ret_m_tu = (
    pe.charts.Line()
        .add_xaxis(Ret_count_m.index.strftime('%Y-%m').tolist())
        .add_yaxis('月退款数量',
                   Ret_count_m.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   )
        .add_yaxis('月退款率',
                   Ret_rate_m.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   )
        .add_yaxis('月退款金额',
                   Ret_money_m.values.tolist(),
                   is_selected=False,
                   is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   )
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ),
                         ),
                         title_opts=opts.TitleOpts(title="月退款情况"),
                         toolbox_opts=opts.ToolboxOpts(),
                         tooltip_opts=opts.TooltipOpts(trigger="axis"),
                         legend_opts=opts.LegendOpts(type_='scroll', pos_top='5%'))
)
Ret_m_tu.render_notebook()

# 客户分层
# 数据导入
Customer_class = pd.read_csv('C:\\Users\\seldo\\Desktop\\dataofmatch\\FRM.csv')
# 数据处理
Customer_class = Customer_class.dropna(axis=1)
Customer_class
Customer_class['CustomerID'] = Customer_class['CustomerID'].astype('object')
Customer_class['Money'] = Customer_class['Money'].astype('int')
Customer_class['RS_class'] = Customer_class['RS_class'].astype('int')
Customer_class['FS_class'] = Customer_class['FS_class'].astype('int')
Customer_class['MS_class'] = Customer_class['MS_class'].astype('int')
Customer_class['Customer_class'] = Customer_class['Customer_class'].astype('int')
# 分数排序
# Customer_class = Customer_class.sort_values(by="Customer_class",ascending= False)
# 统计
Customer_class_count = Customer_class.groupby('Customer_class_name')['CustomerID'].count()
Customer_class_count2 = Customer_class_count.reset_index(name='Customer_class_count')
Customer_class_count2['Rate'] = (Customer_class_count2['Customer_class_count'] / Customer_class_count2[
    'Customer_class_count'].sum()) * 100
# 图
Customer_class_count_tu = (
    pe.charts.Pie()
        .add(
        "客户数目分布",
        [list(z) for z in zip(Customer_class_count.index.tolist(), Customer_class_count.values.tolist())],
        radius=["30%", "75%"],
        # center=["75%", "50%"],
        rosetype="area",
    )
        .set_global_opts(title_opts=opts.TitleOpts(title="客户分层"),
                         toolbox_opts=opts.ToolboxOpts(),
                         legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
                         )
)
Customer_class_count_tu.render_notebook()

Customer_class_rate_tu = (
    pe.charts.Pie()
        .add(
        "",
        [list(z) for z in zip(Customer_class_count2['Customer_class_name'].tolist(),
                              Customer_class_count2['Rate'].astype('int').tolist())],
        radius=["40%", "75%"],
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="客户分层占比"),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_top="15%", pos_left="2%"
        ),
    )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"), )
)
Customer_class_rate_tu.render_notebook()

# 客户分析
Customer_anyl = data[data['Quantity'] > 0].groupby('CustomerID').agg(
    {'InvoiceNo': 'nunique', 'Quantity': 'sum', 'Toa_Pri': 'sum'}).describe()
# 产品的分析
Product_anyl = data[data['Quantity'] > 0].groupby('StockCode').agg(
    {'InvoiceNo': 'nunique', 'Quantity': 'sum', 'Toa_Pri': 'sum'}).describe()

# 消费周期
Buy_interval = data[data['Quantity'] > 0].groupby('CustomerID').apply(
    lambda day: day['InvoiceDate'] - day['InvoiceDate'].shift())
Buy_interval = Buy_interval.dt.days.fillna(0).astype(np.int).reset_index(name='Buy_time_count_wd')
Buy_interval.describe()  # 全部客户
# 提取非0天的周期(老客户)
Buy_interval_have = Buy_interval.replace(0, np.nan).dropna()
Buy_interval_have.describe()
Buy_interval_have_yudata = [[12, 28, 58], ['25%', '50%', '75%']]
Old_custom_day = (
    pe.charts.Pie()
        .add(
        "老客户消费周期",
        [list(z) for z in zip(Buy_interval_have_yudata[1], Buy_interval_have_yudata[0])],
        radius=["30%", "75%"],
        # center=["75%", "50%"],
        rosetype="area",
    )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}天之内"))
        .set_global_opts(title_opts=opts.TitleOpts(title="老客户消费周期"),
                         toolbox_opts=opts.ToolboxOpts(), )
)
Old_custom_day.render_notebook()

# 图导出
page = pe.charts.Page()
page.add(M_count_tu,
         Country_Avg_tu,
         Buy_times_mon_df_tu,
         Buy_times_mon_all_tu,
         Back_buy_count_wm_Ktu,
         Customer_ev_d_tu,
         Customer_ev_w_tu,
         Customer_ev_m_tu,
         Country_tu_sum,
         Sell_d_tu,
         Sell_w_tu,
         Sell_m_tu,
         Week_day_tu,
         Buy_time_count_wtu,
         Buy_time_count_dtu,
         Ret_w_tu,
         Ret_m_tu,
         Customer_class_count_tu,
         Customer_class_rate_tu,
         Old_custom_day,
         )
page.render()
