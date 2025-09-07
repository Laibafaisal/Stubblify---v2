import requests
import datetime
import pandas as pd

OPENWEATHER_API_KEY = '22c148d8d94fe6463b4f23d0f2500616'
API_NINJAS_KEY = '5TZ8k1nJGeIcgz2jNmIHTg==xUhfzjBsaAl5lntd'

def fetch_data(city_name):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    air_url = f"https://api.api-ninjas.com/v1/airquality?city={city_name}"
    headers = {'X-Api-Key': API_NINJAS_KEY}
    air_response = requests.get(air_url, headers=headers)
    airquality_data = air_response.json()

    AT = weather_data['main']['temp']
    RH = weather_data['main']['humidity']
    WS = weather_data['wind']['speed']
    WD = weather_data['wind'].get('deg', 0)

    PM25 = airquality_data.get('PM2.5', {}).get('concentration', 0)

    now = datetime.datetime.now()
    input_data = {
        'WD': WD,
        'RH': RH,
        'WS': WS,
        'AT': AT,
        'PM25': PM25,
        'MONTH': now.month,
        'DAY_OF_YEAR': now.timetuple().tm_yday,
    }

    input_df = pd.DataFrame([input_data])

    return input_data, input_df
