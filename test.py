# coding: utf8
from sqlalchemy import create_engine
import stock_tool
import k_tool
import stock_db_tool
import tushare as ts
import numpy as np
from k_tool import Elem


def x(stock_hists):
    macd_difs, macd_deas, macds = k_tool.macd_cn(np.array([stock_hist.close for stock_hist in stock_hists]), 12, 26, 9)
    elems = [Elem(str(i), e) for i, e in enumerate(macds[-12:len(macds)])]
    stock_hists = stock_hists[-12:len(stock_hists)]
    elems = k_tool.extremum(elems)
    # print(elems)
    # print(k_tool.extremum(elems))
    if len(elems) == 2:
        elem_small = elems[0]
        elem_big = elems[1]
        # macd值 后比前高
        if elem_big.key > elem_small.key:
            # 价格前比后高
            price_before = stock_hists[int(elem_small.key)].close
            price_after = stock_hists[int(elem_big.key)].close
            if price_before > price_after:
                # 最近的macd是正数
                if macds[len(macds)-1:len(macds)][0] > 0:
                    print('----ok:' + stock_hists[0].code)


limit_up_stocks = stock_db_tool.query_all_stocks()
for limit_up_stock in limit_up_stocks:
    stock_hists = stock_db_tool.query_stock_hist(limit_up_stock, 'w', '2015-01-01')
    x(stock_hists)
# print([stock_hist.close for stock_hist in stock_hists])

# print(macds)
# print(macds[-12:len(macds)])
# print(len(macds[-12:len(macds)]))




# break

# df = ts.get_hist_data('600848',start='2016-01-19',ktype='W')
# print(df)
# macd_dif, macd_dea, macd = k_tool.macd_cn(df['close'].values, 12, 26, 9)
# print(macd)
# close = df['close'].values
#
# print(close)


print('------------------------')
# print( [float('%.2f'% item.item()) for item in macd])
print('------------------------')
# print(macdhist)
print('------------------------')
