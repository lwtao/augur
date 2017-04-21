
from sqlalchemy import create_engine
import tushare as ts
import time

engine = create_engine('mysql+pymysql://root:@172.21.104.241/augur?charset=utf8')


def all_stock_code():
    ret = stock_basics()
    # return ['300279']
    return ret.index
    #'603505',
    # return [  '603501',
    #          '603320', '603232', '603229', '603139', '603096', '603081', '600732',
    #          '600710', '300648', '300647', '300645', '300643', '300642', '300554',
    #          '300514', '300372', '002868', '002867', '002866', '002865', '000155',
    #          '000033', '603926', '603920', '603803', '603787']


def stock_basics():
    # code,代码
    # name,名称
    # industry,所属行业
    # area,地区
    # pe,市盈率
    # outstanding,流通股本(亿)
    # totals,总股本(亿)
    # totalAssets,总资产(万)
    # liquidAssets,流动资产
    # fixedAssets,固定资产
    # reserved,公积金
    # reservedPerShare,每股公积金
    # esp,每股收益
    # bvps,每股净资
    # pb,市净率
    # timeToMarket,上市日期
    # undp,未分利润
    # perundp, 每股未分配
    # rev,收入同比(%)
    # profit,利润同比(%)
    # gpr,毛利率(%)
    # npr,净利润率(%)
    # holders,股东人数
    stocks = ts.get_stock_basics()
    return stocks


def hist_data(code, ktype):
    # 参数
    # code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
    # start：开始日期，格式YYYY-MM-DD
    # end：结束日期，格式YYYY-MM-DD
    # ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
    # retry_count：当网络异常后重试次数，默认为3
    # pause:重试时停顿秒数，默认为0
    # 返回值
    # date：日期
    # open：开盘价
    # high：最高价
    # close：收盘价
    # low：最低价
    # volume：成交量
    # price_change：价格变动
    # p_change：涨跌幅
    # ma5：5日均价
    # ma10：10日均价
    # ma20:20日均价
    # v_ma5:5日均量
    # v_ma10:10日均量
    # v_ma20:20日均量
    # turnover:换手率[注：指数无此项]
    start = '2016-10-01'
    if ktype == 'W':
        start = '2014-01-01'
    df = ts.get_hist_data(code, start=start, ktype=ktype)
    df['ktype'] = ktype
    df['code'] = code
    return df


def all_hist_data():

        stock_codes = all_stock_code()
        for stock_code in stock_codes:
            print('-----'+stock_code)
            data_d = hist_data(stock_code, 'D')
            data_w = hist_data(stock_code, 'W')
            save_hist_data(data_d)
            save_hist_data(data_w)
            time.sleep(1)


# return data_d, data_w


def get_data_w(stock_code):
    return hist_data(stock_code, 'W')


def get_data_w_close(stock_code):
    data_w = get_data_w(stock_code)
    close = data_w['close'].values
    return close[:-1]


def save_hist_data(data):
    data.to_sql('hist_data', engine, if_exists='append')


# all_hist_data()
# print(all_stock_code()[3166:])