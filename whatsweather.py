from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import bs4
import requests
from darksky import forecast
from geopy import geocoders
import random

app = Flask(__name__)

def weathernow(nameofcity):
    gn = geocoders.GeoNames(username='amanhirani')
    coordinates = gn.geocode(nameofcity)
    weatherinfo = forecast('873f4066624ce226aba8b4a882829f93',coordinates.latitude ,coordinates.longitude)
    weatherinfo.temperature = ((5 / 9) * (weatherinfo.temperature - 32)) #converting F to C
    # print(weatherinfo.temperature, weatherinfo.summary, weatherinfo.daily.summary,sep= '\n')
    return round(weatherinfo.temperature), weatherinfo.summary, weatherinfo.daily.summary;

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    res2 = requests.get('https://urbandictionary.com/random.php?page=' + (str(random.randrange(1, 99999))))
    respretty2 = bs4.BeautifulSoup(res2.text, "html.parser")
    word = respretty2.select_one('.word').get_text()
    meaning = respretty2.select_one('.meaning').get_text()
    example = respretty2.select_one('.example').get_text()

    body = request.values.get('Body', None)

    resp = MessagingResponse()
    mess1 = 'hi'
    if body == 'hello':
        resp.message(mess1)
    elif body == 'bye':
        resp.message("Goodbye")
    elif body == 'dicktionary':
        resp.message('Word: ' + str(word).upper() + ' ' +
                     '  Meaning: ' +
                     str(meaning) + ' \n Example: ' + str(example))
    elif body == 'weather':
        # resp.message(str(weathertoday()))
        resp.message(str(weathernow(nameofcity='wollongong')))
    else:
        resp.message(str(weathernow(nameofcity=(body))))
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
