import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd
import numpy as np
#import pandas_datareader.data as web
from datetime import datetime
import talib
import joblib
# start = datetime(2000, 1, 1) # or start = '1/1/2016'
#end = datetime.today()
#stock_name ='000001.sz'
#prices = web.DataReader(stock_name, 'yahoo', start, end)
#prices.index = [ i.strftime("%Y-%m-%d") for i in prices.index]
# prices.to_csv(r'C:\Users\86188\Desktop\young\黄鑫润'+'\\'+stock_name.split('.')[0]+'.csv')
import os
os.chdir('process/')

def setDF(path):
    prices = pd.read_csv(path, index_col=0)
    prices = prices.rename(
        columns={'high': 'High', 'low': 'Low', 'close': 'Close'})
    close = pd.DataFrame(prices['Close'])
    close.index = prices.index
    close.set_index(pd.to_datetime(close.index)).plot()
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


def trainModel():
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
    joblib.dump(model_gbr_disorder, company+"_model.m")
    return model_gbr_disorder, y_predict


################
def setStock_Index():
    new_y = y_predict[-268:-7]
    stock_index = pd.DataFrame(df[-268:-7]['close'])
    #stock_index = pd.DataFrame(df[-len(y_predict):]['close'])
    ##stock_index.index = prices.index[-983:]
    stock_index['updown'] = new_y

    rate = stock_index['close'] / stock_index['close'].shift(1)
    rate.fillna(1, inplace=True)
    stock_index['rate'] = rate
    stock_index['rate'][stock_index['updown'] == 0] = 1

    stock_index['asset'] = stock_index['rate'].cumprod()
    stock_index.to_csv("stock_" + company + ".csv")
    # df.to_csv("df.csv")
    return stock_index


def plot_feature_importances(feature_importances, title, feature_names):
    #     将重要性值标准化
    feature_importances = 100.0*(feature_importances/max(feature_importances))
    #     将得分从高到低排序
    index_sorted = np.flipud(np.argsort(feature_importances))
    #     让X坐标轴上的标签居中显示
    pos = np.arange(index_sorted.shape[0])+0.5

    # plt.figure(figsize=(14, 6))
    # plt.bar(pos, feature_importances[index_sorted], align='center')
    # plt.xticks(pos, feature_names[index_sorted])
    # plt.ylabel('Relative Importance')
    # plt.title(title)
    # plt.show()

# plot_feature_importances(model_gbr_disorder.feature_importances_,
 #                        'Random Forest Classifer', df.columns[1:])


def plot_Asset(stock_index):
    # 画指数
    ax = (stock_index['asset']-1).plot(legend=None)  # 横坐标
    # ax = (stock_index['Close']/stock_index['Close'][0]-1).plot(title = '恒生收益情况',legend=None)  #横坐标

    ax.set_xticks(range(0, len(stock_index['close'].index)), 100)
    ax.set_xticklabels(stock_index['close'].index[::100], rotation=30)
    ax.set_xlabel("Time")
    ax.set_ylabel("Return")
    ax.grid(True)

# plot_Asset(stock_index)

# 回测/计算各个指标（跟hs指数对比）最大回撤/年华收益率/夏普比率/信息比率


def sharpe_ratio(return_list):
    '''夏普比率'''
    df = return_list
    #    df = pd.DataFrame(return_list)
    total_ret = df[df.index[-1]]-1
    annual_ret = pow(1+total_ret, 252/len(df))-1
    annual_std = df.std()
    sharpe_ratio = (annual_ret-0.02) * np.sqrt(252) / \
        annual_std  # 默认252个工作日,无风险利率为0.02
    return annual_ret, sharpe_ratio


def info_ratio(return_list):
    '''信息比率'''
    df = return_list
    #    df = pd.DataFrame(return_list)
    total_ret = df[df.index[-1]]-1
    annual_ret = pow(1+total_ret, 252/len(df))-1
    annual_std = df.std()
    info_ratio = (annual_ret+0.005) * np.sqrt(252) / \
        annual_std  # 默认252个工作日,无风险利率为0.02
    return info_ratio


def MaxDrawdown(a):
    '''最大回撤率'''
    i = np.argmax((np.maximum.accumulate(a) - a) /
                  np.maximum.accumulate(a))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(a[:i])  # 开始位置
    return (a[j] - a[i]) / (a[j])

#sr = sharpe_ratio(stock_index['asset'])
#ir = info_ratio(stock_index['asset'])
#md = MaxDrawdown(stock_index['asset'])


dic = {'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Google': 'GOOG', 'Amazon': 'AMZN', 'Facebook': 'FB', 'Tesla': 'TSLA',
       'Berkshire Hathaway': 'BRK-A', 'Tencent': 'TCEHY', 'TSMC': 'TSM', 'NVIDIA': 'NVDA', 'Visa': 'V', 'JPMorgan Chase': 'JPM',
       'Alibaba': 'BABA', 'Johnson&Johnson': 'JNJ', 'UnitedHealth': 'UNH', 'Samsung': 'SMSN.LON', 'Walmart': 'WMT', 'Bank of America': 'BAC',
       'LVMH': 'LVMUY', 'Home Depot': 'HD', 'Kweichow Moutai': '600519.SHH', 'Mastercard': 'MA', 'Procter&Gamble': 'PG',
       'Nestle': 'NSRGY', 'Roche': 'RHHBY', 'ASML': 'ASML', 'Walt Disney': 'DIS', 'Paypal': 'PYPL', 'Adobe': 'ADBE', 'Salesforce': 'CRM'}
company_name_list = ['Apple', 'Microsoft', 'Google', 'Amazon', 'Facebook', 'Tesla',
                     'Berkshire Hathaway', 'Tencent', 'TSMC', 'NVIDIA', 'Visa', 'JPMorgan Chase',
                     'Alibaba', 'Johnson&Johnson', 'UnitedHealth', 'Samsung', 'Walmart', 'Bank of America',
                     'LVMH', 'Home Depot', 'Kweichow Moutai', 'Mastercard', 'Procter&Gamble',
                     'Nestle', 'Roche', 'ASML', 'Walt Disney', 'Paypal', 'Adobe', 'Salesforce']

proposalAddCompanySymbol = []
for i in range(30):
    company = dic[company_name_list[i]]
    print(company)

    path = r'processed_' + company + '.csv'
    df = setDF(path)
    model_gbr_disorder, y_predict = trainModel()
    stock_index = setStock_Index()
    if(df.iat[-1, 1] > 0):
        stock_index.iat[-1, 3]
        proposalAddCompanySymbol.append(company)



def findRecommend():
    proposalAsset = []
    for proposalSymbol in proposalAddCompanySymbol:
        path1 = r'stock_' + proposalSymbol + '.csv'
        stockAsset = pd.read_csv(path1, index_col=0)
        proposalAsset.append(stockAsset.iat[-1, 3])
    
    stock_tuples=list(zip(proposalAddCompanySymbol, proposalAsset))  

    sort_stock_tuples = sorted(stock_tuples, key=lambda stockTuple: stockTuple[1], reverse=True)
    return sort_stock_tuples


company_name = 'Walt Disney'
def chooseOneStock(company_name):
    company_label = dic[company_name]
    path = r'processed_' + company_label + '.csv'
    df = setDF(path)
    
    clf = joblib.load(company_label + "_model.m")
    x = df.iloc[-1:, 2:13].values
    up_down = clf.predict(x)
   
    closePrice = df.iat[-1, 0]
       
    sort_stock_tuples = findRecommend()

    return closePrice, up_down, sort_stock_tuples[0:5] 

closePrice, up_down, sort_stock_tuples1 = chooseOneStock(company_name)    
print(closePrice) 
print(up_down)
print(sort_stock_tuples1)

