from flask import Flask, request, make_response
import os , json
from pyowm import OWM
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
key = '2af3344928fc1e5f8e70e452fc85a56d'
owm = OWM(key)


@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req))
    res = process(req)
    res = json.dumps(res)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def process(req):
    result = req.get("queryResult")
    param = result.get('parameters')
    city = param.get('city_name')
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    print(w)
    temp = w.get_temperature('celsius')
    mintemp = str(temp.get('temp_min'))
    maxtemp = str(temp.get('temp_max'))
    ctemp=str(temp.get('temp'))

    wind_res = w.get_wind()
    wind = str(wind_res.get('speed'))

    speech= "Today the weather in " + city + ' is \n'+'Climate = '+str(w.get_detailed_status())+": \n" + "Temperature = "+ctemp+\
            "\N{DEGREE SIGN}C\n Min_Temp = "+mintemp+"\N{DEGREE SIGN}C \nMax_Temp = "+maxtemp+"\N{DEGREE SIGN}C\nWind = "\
    +wind + 'm/s'
    return {
        "fulfillmentText": speech,
        "displayText": speech
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(host='0.0.0.0', debug=False, port=port)
