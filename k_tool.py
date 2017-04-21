import talib as tl
import numpy as np
import functools

def macd_cn(close, fast_period, slow_period, signal_period):
    # short_win = 12    # 短期EMA平滑天数
    # long_win  = 26    # 长期EMA平滑天数
    # macd_win  = 20     # DEA线平滑天数
    macd_dif, macd_dea, macd = tl.MACDEXT(close, fastperiod=fast_period, fastmatype=1, slowperiod=slow_period,
                                             slowmatype=1, signalperiod=signal_period, signalmatype=1)
    macd = macd * 2
    return macd_dif, macd_dea, macd

# 同花顺和通达信等软件中的SMA
def SMA_CN(close, timeperiod) :
    close = np.nan_to_num(close)
    return functools.reduce(lambda x, y: ((timeperiod - 1) * x + y) / timeperiod, close)

# 同花顺和通达信等软件中的KDJ
def KDJ_CN(high, low, close, fastk_period, slowk_period, fastd_period) :
    kValue, dValue = tl.STOCHF(high, low, close, fastk_period, fastd_period=1, fastd_matype=0)

    kValue = np.array(map(lambda x : SMA_CN(kValue[:x], slowk_period), range(1, len(kValue) + 1)))
    dValue = np.array(map(lambda x : SMA_CN(kValue[:x], fastd_period), range(1, len(kValue) + 1)))

    jValue = 3 * kValue - 2 * dValue

    func = lambda arr : np.array([0 if x < 0 else (100 if x > 100 else x) for x in arr])

    kValue = func(kValue)
    dValue = func(dValue)
    jValue = func(jValue)
    return kValue, dValue, jValue

# 同花顺和通达信等软件中的RSI
def RSI_CN(close, timeperiod) :
    diff = map(lambda x, y : x - y, close[1:], close[:-1])
    diffGt0 = map(lambda x : 0 if x < 0 else x, diff)
    diffABS = map(lambda x : abs(x), diff)
    diff = np.array(diff)
    diffGt0 = np.array(diffGt0)
    diffABS = np.array(diffABS)
    diff = np.append(diff[0], diff)
    diffGt0 = np.append(diffGt0[0], diffGt0)
    diffABS = np.append(diffABS[0], diffABS)
    rsi = map(lambda x : SMA_CN(diffGt0[:x], timeperiod) / SMA_CN(diffABS[:x], timeperiod) * 100
              , range(1, len(diffGt0) + 1) )

    return np.array(rsi)


class Elem():
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return self.key+'-'+str(self.value)

    def __repr__(self):
        return self.key+'-'+str(self.value)


# 求极值  type=1表示极小值 type=2表示极大值
def extremum(elems, type=1):
    extremum_elems = [];
    for i in range(len(elems)):
        if i != 0 and i != len(elems) - 1:
            if elems[i].value < elems[i - 1].value:
                if elems[i].value < elems[i + 1].value:
                    extremum_elems.append(elems[i])

    # print('--------------')
    # print(extremum_elems)
    if len(extremum_elems) >= 2:
        extremum_elems.sort(key=elem_sort_key)
        return extremum_elems[:2]
    return []


def elem_sort_key(item):
    return item.value


# elems = [Elem('k1', 14), Elem('k2', 6), Elem('k3', 4), Elem('k4', 10), Elem('k5', 14), Elem('k6', 4), Elem('k7', 2),
#          Elem('k8', 9), Elem('k9', 1), Elem('k10', 19)]
# print(extremum(elems))
