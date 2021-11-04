import joblib
import pandas as pd
import talib
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier

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
    # temp = prices['Close']/prices['Close'].shift(1)
    # temp = prices['open'].shift(-2) / prices['open'].shift(-1)
    temp = prices['Close'] / prices['Close'].shift(1)
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

def cul_accuracy_precision_recall(y_true, y_pred, pos_label=1):
    accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
    recall = recall_score(y_true=y_true, y_pred=y_pred, pos_label=pos_label)
    precision = precision_score(
        y_true=y_true, y_pred=y_pred, pos_label=pos_label)
    F1 = 2 / ((1 / precision) + (1 / recall))
    return {"accuracy": float("%.5f" % accuracy),
            "precision": float("%.5f" % precision),
            "recall": float("%.5f" % recall),
            "F1": float("%.5f" % F1)
            }

    #from sklearn import svm
    #from sklearn.model_selection import train_test_split
    #from sklearn.metrics import accuracy_score


def trainModel(df,company):
    y, x = np.split(df.iloc[:, 1:].values, (1,), axis=1)

    train_ratio = 0.7
    cut = int(len(y) * train_ratio)
    x_train, x_test, y_train, y_test = x[:cut], x[cut:], y[:cut], y[cut:]
    # print(len(y_train))
    #svm_model = svm.SVC(C=0.5, kernel='linear')
    ## svm_model = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
    #svm_model.fit(x_train, y_train.ravel())
    # print(accuracy_score(y_train,svm_model.predict(x_train)))
    #print('Accuracy:', accuracy_score(y_test, svm_model.predict(x_test)))
    #
    #
    #svm_evaluation = cul_accuracy_precision_recall(y_test, svm_model.predict(x_test))
    # print(y_test.ravel())
    # print(svm_model.predict(x_test))

    model_gbr_disorder = RandomForestClassifier()
    model_gbr_disorder.fit(x_train, y_train.ravel())
    gbr_score_disorder = model_gbr_disorder.score(x_test, y_test.ravel())
    y_predict = model_gbr_disorder.predict(x_test)
    rf_evaluation = cul_accuracy_precision_recall(y_test, y_predict)
    print(rf_evaluation)
    joblib.dump(model_gbr_disorder, 'model/'+company+"_model.m")
    return model_gbr_disorder, y_predict

dic = {'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Google': 'GOOG', 'Amazon': 'AMZN', 'Facebook': 'FB', 'Tesla': 'TSLA',
       'Berkshire Hathaway': 'BRK-A', 'Tencent': 'TCEHY', 'TSMC': 'TSM', 'NVIDIA': 'NVDA', 'Visa': 'V', 'JPMorgan Chase': 'JPM',
       'Alibaba': 'BABA', 'Johnson&Johnson': 'JNJ', 'UnitedHealth': 'UNH', 'Samsung': '005930.KS', 'Walmart': 'WMT', 'Bank of America': 'BAC',
       'LVMH': 'LVMUY', 'Home Depot': 'HD', 'Kweichow Moutai': '600519.SS', 'Mastercard': 'MA', 'Procter&Gamble': 'PG',
       'Nestle': 'NSRGY', 'Roche': 'RHHBY', 'ASML': 'ASML', 'Walt Disney': 'DIS', 'Paypal': 'PYPL', 'Adobe': 'ADBE', 'Salesforce': 'CRM'}
company_name_list = ['Apple', 'Microsoft', 'Google', 'Amazon', 'Facebook', 'Tesla',
                     'Berkshire Hathaway', 'Tencent', 'TSMC', 'NVIDIA', 'Visa', 'JPMorgan Chase',
                     'Alibaba', 'Johnson&Johnson', 'UnitedHealth', 'Samsung', 'Walmart', 'Bank of America',
                     'LVMH', 'Home Depot', 'Kweichow Moutai', 'Mastercard', 'Procter&Gamble',
                     'Nestle', 'Roche', 'ASML', 'Walt Disney', 'Paypal', 'Adobe', 'Salesforce']
annual_list = []
for i in range(30):
    symbol = dic[company_name_list[i]]
    path = r'processed data/processed_' + symbol + '.csv'
    daf = setDF(path)
    model_gbr_disorder, y_predict = trainModel(daf,symbol)
    new_y = y_predict[-353:-100]
    stock_index = pd.DataFrame(daf[-353:-100]['close'])
    # stock_index = pd.DataFrame(df[-len(y_predict):]['close'])
    ##stock_index.index = prices.index[-983:]
    stock_index['updown'] = new_y

    rate = stock_index['close'] / stock_index['close'].shift(1)
    rate.fillna(1, inplace=True)
    stock_index['rate'] = rate
    stock_index['rate'][stock_index['updown'] == 0] = 1

    stock_index['asset'] = stock_index['rate'].cumprod()
    annual_list.append(stock_index.iloc[-1]['asset'])
annual_df = pd.DataFrame(np.array(annual_list).reshape(30,1))
new_col=['rate']
annual_df.columns=new_col
annual_df['name']=company_name_list
annual_df.to_csv('process/annual_return.csv')