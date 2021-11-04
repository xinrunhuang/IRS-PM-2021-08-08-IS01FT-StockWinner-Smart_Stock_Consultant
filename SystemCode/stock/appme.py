from flask import Flask, request, make_response, jsonify
import requests
import pandas as pd
from company import company_cla_list
# from stock import findRecommend
# from stock import chooseOneStock
from requests import Session
import json
from predict import predict_company,recommend_companies
app = Flask(__name__)


# **********************
# UTIL FUNCTIONS : START
# **********************

# def getjson(url):
#     resp = requests.get(url)
#     return resp.json()


def getStockInfo(company):
    for i in range(30):
        if(company_cla_list[i].name==company):
            price=company_cla_list[i].price
            break
    return price

def getupordownInfo(company):
    for i in range(30):
        if (company_cla_list[i].name == company):
            upordown= predict_company(company_cla_list[i].name)[0]
            break
    return upordown


def getbuyInfo(company):
    up_down=getupordownInfo(company)
    return up_down
# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************


def getStockIntentHandler(company):
    """
    Get location parameter from dialogflow and call the util function `getWeatherInfo` to get weather info
    """
    #location = location.lower()
    price = getStockInfo(company)
    return f"Currently in {company} , its stock price is {price} ."

def getupordownIntentHandler(company):
    upordown = getupordownInfo(company)
    if upordown == 0:
        stock1 = "down"
    else:
        stock1 = "up"
    return f"Currently in {company} , its stock price is {stock1}."

def getbuyIntentHandler(company):
    up_down=getbuyInfo(company)
    # up_down=up_down[0]
    if up_down == 0:
        return f"Currently in {company}, we don't recommend you to buy it"
    else:
        return f"Currently in {company}, we recommend you to buy it"

# ***************************
# Intent Handlers funcs : END
# ***************************


# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************
@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == "GetStockIntent":
        company = req["queryResult"]["parameters"]["comname"]
        print(company)
        respose_text = getStockIntentHandler(company)
    elif intent_name == "GetupordownIntent":
        company = req["queryResult"]["parameters"]["comname"]
        print(company)
        respose_text = getupordownIntentHandler(company)
    elif intent_name == "GetbestIntent":
        sort_stock_tuples = recommend_companies()
        best1 = sort_stock_tuples[0][0]
        best2 = sort_stock_tuples[1][0]
        best3 = sort_stock_tuples[2][0]
        best=[]
        best.append(best1)
        best.append(best2)
        best.append(best3)
        respose_text = "The top three choices are: "
        for i in range(5):
            respose_text = respose_text + sort_stock_tuples[i][0] + ' '
    elif intent_name == "GetbuyIntent":
        company = req["queryResult"]["parameters"]["comname"]
        print(company)
        respose_text = getbuyIntentHandler(company)
    else:
        respose_text = "Unable to find a matching intent. Try again."
    print(respose_text)
    return make_response(jsonify({'fulfillmentText': respose_text}))

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)