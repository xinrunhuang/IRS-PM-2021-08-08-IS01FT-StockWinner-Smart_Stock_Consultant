import pandas as pd
import talib


def setDF(path):
    prices = pd.read_csv(path, index_col=0)
    prices = prices.rename(
        columns={'high': 'High', 'low': 'Low', 'close': 'Close'})
    close = pd.DataFrame(prices['Close'])
    close.index = prices.index
    # close.set_index(pd.to_datetime(close.index)).plot()
    #close = close[:-15]
    df = pd.DataFrame()
    df['close'] = prices['Close']
    # 计算y
    temp = prices['Close']/prices['Close'].shift(1)
    temp[temp > 1] = 1
    temp[temp < 1] = 0
    df['up_down'] = temp

    # 计算ma
    temp = talib.MA(prices['Close'], timeperiod=10, matype=0)
    temp = temp - prices['Close']
    temp[temp > 0] = 1
    temp[temp < 0] = 0
    df['MA'] = temp

    # 计算布林带

    temp = talib.BBANDS(prices['Close'], timeperiod=5,
                        nbdevup=2, nbdevdn=2, matype=0)[1]
    temp = temp - prices['Close']
    temp[temp > 0] = 1
    temp[temp < 0] = 0
    df['PSY'] = temp

    # aroon

    temp0 = talib.AROON(prices['High'], prices['Low'], timeperiod=14)[0]
    temp1 = talib.AROON(prices['High'], prices['Low'], timeperiod=14)[1]

    temp0[temp0 > 70] = 1
    temp0[temp0 < 70] = 0
    temp1[temp1 > 70] = 0
    temp1[temp1 < 70] = 1

    df['AROON_Up'] = temp0
    df['AROON_Down'] = temp1

    # CCI
    temp = talib.CCI(prices['High'], prices['Low'],
                     prices['Close'], timeperiod=14)
    te_temp = (temp/temp.shift(1))[(temp <= 200) & (temp >= -200)]
    temp[te_temp[te_temp > 1].index] = 1
    temp[te_temp[te_temp < 1].index] = 0

    temp[temp > 200] = 1
    temp[temp < -200] = 0
    df['CCI'] = temp

    # cmo

    temp = talib.CMO(prices['Close'], timeperiod=14)
    temp[temp > 0] = 1
    temp[temp < 0] = 0
    df['CMO'] = temp

    # macd
    temp0 = talib.MACD(prices['Close'], fastperiod=12,
                       slowperiod=26, signalperiod=9)[0]
    temp1 = talib.MACD(prices['Close'], fastperiod=12,
                       slowperiod=26, signalperiod=9)[1]

    temp = temp0 - temp1
    temp[temp > 0] = 1
    temp[temp < 0] = 0
    df['MACD'] = temp

    # RSI
    temp = talib.RSI(prices['Close'], timeperiod=14)
    temp[temp > 50] = 1
    temp[temp <= 50] = 0
    df['RSI'] = temp

    ########
    temp0, temp1 = talib.STOCH(prices['High'], prices['Low'], prices['Close'],
                               fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    temp0 = temp0/temp0.shift(1)
    temp1 = temp1/temp1.shift(1)
    temp0[temp0 > 1] = 1
    temp0[temp0 < 1] = 0
    temp1[temp1 > 1] = 1
    temp1[temp1 < 1] = 0

    df['STOCHK'] = temp0
    df['STOCHD'] = temp1

    ########
    temp = talib.WILLR(prices['High'], prices['Low'],
                       prices['Close'], timeperiod=14)
    temp = temp/temp.shift(1)
    temp[temp > 1] = 1
    temp[temp < 1] = 0
    df['BIAS'] = temp

    # df.describe()
    # df.hist(figsize=(20,15))

    df.dropna(how='any', inplace=True)
    return df