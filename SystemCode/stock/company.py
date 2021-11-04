import pandas as pd
import numpy as np
from predict import predict_company,recommend_companies
company_name_list=['Apple','Microsoft','Google','Amazon','Facebook','Tesla',
                   'Berkshire Hathaway','Tencent','TSMC','NVIDIA','Visa','JPMorgan Chase',
                   'Alibaba','Johnson&Johnson','UnitedHealth','Samsung','Walmart','Bank of America',
                   'LVMH','Home Depot','Kweichow Moutai','Mastercard','Procter&Gamble',
                   'Nestle','Roche','ASML','Walt Disney','Paypal','Adobe','Salesforce']
company_symbol_list=['AAPL','MSFT','GOOG','AMZN','FB','TSLA','BRK-A','TCEHY','TSM',
                     'NVDA','V','JPM','BABA','JNJ','UNH','005930.KS','WMT','BAC','LVMUY',
                     'HD','600519.SS','MA','PG','NSRGY','RHHBY','ASML','DIS','PYPL','ADBE','CRM']
company_marketcap_list=[2422,2309,1904,1745,945.47,871.65,641.06,614.76,598.15,553.77,506.13,492.20,452.23,
                        421.51,400.38,400.33,395.07,381.40,380.17,374.66,353.69,351.49,345.64,343.09,340.72,
                        325.79,317.64,310.98,296.34,285.57]

img_sml_path='/static/images/company_small/'
img_lar_path='/static/images/company_large/'
trend_flag = True
predict_up_companies = recommend_companies()
class Company:

    def __init__(self,id,name,symbol,price,market,trend,smlpic,larpic,prediction,change,annual):
        self.id=id
        self.name=name
        self.symbol=symbol
        self.price=price
        self.market=market
        self.trend=trend
        self.prediction=prediction
        self.smlpic = smlpic
        self.larpic = larpic
        self.change = change
        self.annual = annual
company_cla_list=[]
annual_return = pd.read_csv('./process/annual_return.csv')
for i in range(30):
    id = i+1
    name = company_name_list[i]
    symbol = company_symbol_list[i]
    data = pd.read_csv('./processed data/processed_' + symbol + '.csv')  # get the data


    market=company_marketcap_list[i]
    trend_yesterday = data.iloc[-31]['close']
    trend_now = data.iloc[-1]['close']
    price = trend_now
    trend_yes = data.iloc[-2]['close']
    trend_rate = trend_now / trend_yes
    if trend_yesterday > trend_now:
        trend_flag = False  ##the stock price is going down
    else:
        trend_flag = True
    trend = trend_flag
    smlpic = img_sml_path+symbol+'.png'
    # print(smlpic)
    larpic = img_lar_path+symbol+'.png'
    # print(larpic)
    annual = annual_return.iloc[i]['rate']
    change = str(round((trend_rate-1)*100,4)) + '%'
    prediction = predict_company(company_name_list[i])[0]

    co = Company(id=id,name=name,symbol=symbol,price=price,market=market,trend=trend,smlpic=smlpic,larpic=larpic,prediction=prediction,annual=annual,change=change)
    company_cla_list.append(co)
# print()
# print(len(company_marketcap_list))
# name = "1,2,3,4"
# nameid = name.split(",")
# respon = {
#               'output': [
#                 {
#                   "type": "text",
#                   "value": 'hello'
#                 }
#               ]
#             }
# testj = json.dumps(respon)
# print(respon)
# print(type(nameid))
# for c in nameid:
#     i = int(c)
#     print(type(i))