from flask import Flask, render_template, request, redirect, url_for, Response,jsonify,make_response
import json
from company import company_cla_list,predict_up_companies
app = Flask("stock",static_folder="static/" ,template_folder="templates/")
from chatbot import chat_stock
from app import getWeatherInfo, getWeatherIntentHandler
from predict import predict_company,recommend_companies
def getStockInfo(company):
    for i in range(30):
        if(company_cla_list[i].name==company or company==company_cla_list[i].name.lower()):
            price=company_cla_list[i].price
            break
    return price

def getupordownInfo(company):
    for i in range(30):
        if (company_cla_list[i].name == company or company == company_cla_list[i].name.lower()):
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
    return f"Currently in {company} , its stock price is going to go {stock1}."

def getbuyIntentHandler(company):
    up_down=getbuyInfo(company)
    # up_down=up_down[0]
    if up_down == 0:
        return f"Currently in {company}, the stock is predicted to go down, we don't recommend you to buy it"
    else:
        return f"Currently in {company}, the stock is predicted to go up, we recommend you to buy it"


@app.route('/')
def hello_world():

    return render_template('index.html',companies=company_cla_list)


@app.route('/searchresult/<comname>')
def searchresult(comname):
    ids = comname.split(',')
    company_list = []
    for i in ids:
        company_list.append(company_cla_list[int(i)-1])
    return render_template('index.html',companies=company_list)


@app.route('/detail/<int:num>')
def stock_pre(num):

    print(num)
    comany_list=[]
    comany_list.append(company_cla_list[num-1])
    return render_template('stock_detail.html',company=comany_list)

@app.route('/pred-companies/<comname>')
def precompanies(comname):
    ids = comname.split(',')
    company_list = []
    for i in ids:
        company_list.append(company_cla_list[int(i)-1])
    return render_template('stock_detail.html',company=company_list)

@app.route('/predicall')
def prediall():

    return render_template('stock_detail.html',company=company_cla_list)

@app.route('/search',methods=['POST'])
def searchcom():
    companyid = request.form['name']
    # print(type(companyid))
    return companyid

@app.route('/chat',methods=['GET'])
def chatstock():
    # print('adc')
    que = request.args.get('text')
    print(que)
    respon = {"output":[{"type":"text","value":chat_stock(que)}]}
    return Response(json.dumps(respon),  mimetype='application/json')

@app.route('/google', methods=['POST'])
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
        sort_stock_tuples = predict_up_companies
        best1 = sort_stock_tuples[0][0]
        best2 = sort_stock_tuples[1][0]
        best3 = sort_stock_tuples[2][0]
        best = []
        best.append(best1)
        best.append(best2)
        best.append(best3)
        respose_text = "The top 3 recommended stocks are: "
        for i in range(3):
            respose_text = respose_text + sort_stock_tuples[i][0] + ' '
    elif intent_name == "GetbuyIntent":
        company = req["queryResult"]["parameters"]["comname"]
        print(company)
        respose_text = getbuyIntentHandler(company)
    else:
        respose_text = "Unable to find a matching intent. Try again."
    print(respose_text)
    return make_response(jsonify({'fulfillmentText': respose_text}))

if __name__ == '__main__':
    app.run(debug=True)