from flask import Flask, request, make_response, jsonify
import requests
from requests import Session
import json

headers = {
	'Accepts': 'application/json',
	'X-CMC_PRO_API_KEY': '6cbb4261-6f80-424b-8423-04d768397ef9',
}

session = Session()
session.headers.update(headers)
app = Flask('stock')
## TODO: STEP 1 
APIKEY = "0753e43ef70a0218a246c04f162567ea" # Place your API KEY Here... 
#"8a81d247d650cb16469c4ba3ceb7d265"

# **********************
# UTIL FUNCTIONS : START
# **********************

def windspeed(speed):
    if speed < 0.3:
        description = "calm"
    elif speed < 1.5:
        description = "light air"
    elif speed < 3.3:
        description = "light breeze"
    elif speed < 5.5:   
        description = "gentle breeze"
    elif speed < 8.0:
        description = "moderate breeze"
    elif speed < 10.8:
        description = "fresh breeze"
    elif speed < 13.9:
        description = "strong breeze"
    elif speed < 17.2:
        description = "near gale"
    elif speed < 20.7:
        description = "gale"
    elif speed < 24.5:
        description = "severe gale"
    elif speed < 28.4:
        description = "storm"
    elif speed < 32.6:
        description = "violent storm"
    else:
        description = "hurricane"
    return description

def getjson(url):
    resp = requests.get(url)
    return resp.json()


def getWeatherInfo(location):
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
    print(API_ENDPOINT)
    data = getjson(API_ENDPOINT)
    weather = []
    weather.append(data["weather"][0]["description"])
    weather.append(data["main"]["temp"] - 273.16)
    wind = data["wind"]["speed"]
    weather.append(windspeed(wind))
    print("weather is "+str(weather))

    return weather
# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************


def getWeatherIntentHandler(location):
    """
    Get location parameter from dialogflow and call the util function `getWeatherInfo` to get weather info
    """
    location = location.lower()
    weather = getWeatherInfo(location)
    temp = round(weather[1],2)
    return f"Currently in {location} , it is {weather[0]} .The temperature is {temp} degrees centigrade and wind level is {weather[2]}."

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
    location = req["queryResult"]["parameters"]["locname"]
    print(location)
    if intent_name == "GetWeatherIntent":
        respose_text = getWeatherIntentHandler(location)
    else:
        respose_text = "Unable to find a matching intent. Try again."
    return make_response(jsonify({'fulfillmentText': respose_text}))

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)