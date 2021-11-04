import joblib
import pandas as pd

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

from prepare import setDF
def predict_company(company_name):
    company_label = dic[company_name]
    path = r'processed data/processed_' + company_label + '.csv'
    df = setDF(path)
    clf = joblib.load('model/'+ company_label + "_model.m")
    x = df.iloc[-1:, 2:13].values
    up_down = clf.predict(x)
    return up_down

def recommend_companies():
    proposal = {}
    annual_return = pd.read_csv('process/annual_return.csv')
    recommended = []

    for i in range(30):
        up_down = predict_company(company_name_list[i])[0]
        if up_down>0:
            proposal[company_name_list[i]] = annual_return.iloc[i]['rate']
    proposal_order = sorted(proposal.items(), key=lambda x: x[1], reverse=True)
    # proposal_order = list(proposal_order.key())
    for i in range(5):
        recommended.append(proposal_order[i])
    return recommended

re = recommend_companies()
# print(re[0][0])
# proposal = {}
# annual_return = pd.read_csv('process/annual_return.csv')
# recommended = []
#
# for i in range(30):
#     up_down = predict_company(company_name_list[i])[0]
#     if up_down > 0:
#         proposal[company_name_list[i]] = annual_return.iloc[i]['rate']
#         # annual.append(annual_return.iloc[i]['rate'])
# proposal_order = sorted(proposal.items(),key=lambda x:x[1],reverse=False)
# for i in range(5):
#     recommended.append(proposal_order[i])

# print(type(annual[1]))
# for i in range(30):
#     print(predict_company(company_name_list[i])[0])
# flag = predict_company('Apple')
# print(flag[0])