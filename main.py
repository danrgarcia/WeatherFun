import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn
from secrets import API_KEY
import requests
import time
import logging
from citipy import citipy
import json

def get_weather_data(coords, time_between=1):
    """ Queries openweather API for data.

    Args:
        coords: A Pandas Dataframe with rows containing 'latitude'
            and 'longitude' columns.
        time_between: An integer specifying the sleep time in seconds
            between each API ping. Defaults to the OpenWeatherAPI's
            recommended limit of 1 request per second.

    Returns:
        A list of nested dicts (loaded JSON results).
    """

    results = []
    for ind, row in coords.iterrows():
        lat, lon = row['latitude'], row['longitude']
        query = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
        print(query)
        clean_url = query.rpartition("&")[0]

        city = citipy.nearest_city(lat, lon)
        logger.info(f"Call {ind}: {city.city_name} {clean_url}")

        result = requests.get(query)
        results.append(result.json())
        time.sleep(time_between)
    return results

#Set up a logger
logger = logging.getLogger('weather')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('api_calls.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


seaborn.set()

#Retrieve our 500 random lat/long sets
np.random.seed(125)
lats = np.random.randint(-90, 90, size=500)
longs = np.random.randint(-180, 180, size=500)
coords = pd.DataFrame({
    "latitude": lats,
    "longitude": longs
})

#print(coords.head())

#plt.hist(coords['latitude'])
#plt.show()

#plt.hist(coords['longitude']o)
#plt.show()

full_results = get_weather_data(coords)
print(full_results[:3])

with open("weather.json", "w") as outfile:
    json.dump(full_results, outfile)

important_json_data = []
for point in full_results:
    lat = point['coord']['lat']
    lon = point['coord']['lon']
    temp = point['main']['temp']
    humidity = point['main']['humidity']
    cloudiness = point['clouds']['all']
    wind =point['wind']['speed']


    row = [lat, lon, temp, humidity, cloudiness, wind]
    important_json_data.append(row)

weather_df = pd.DataFrame(important_json_data)
weather_df.columns = [
    "latitude",
    "longitude",
    "temperature",
    "humidity",
    "clouds",
    "wind",
]
weather_df.head()

weather_df.to_csv("weather.csv"
                  "")

plt.scatter(weather_df.temperature, weather_df.latitude)
plt.xlabel("Temperature (F)")
plt.ylabel("Latitude (degrees)")
plt.title("Temperature vs. Latitude")
plt.show()

plt.scatter(weather_df.humidity, weather_df.latitude)
plt.xlabel("Humidity (%)")
plt.ylabel("Latitude (degrees)")
plt.title("Humidity vs. Latitude")
plt.show()

plt.scatter(weather_df.clouds, weather_df.latitude)
plt.xlabel("Cloudiness (%)")
plt.ylabel("Latitude (degrees)")
plt.title("Cloudiness vs. Latitude")
plt.show()

plt.scatter(weather_df.clouds, weather_df.longitude)
plt.xlabel("Longitude (degrees)")
plt.ylabel("Cloudiness (%)")
plt.title("Longitude vs. Cloudiness")
plt.show()

plt.scatter(weather_df.wind, weather_df.latitude)
plt.xlabel("Wind Speed (mph (abs))")
plt.ylabel("Latitude (degrees)")
plt.title("Wind Speed vs. Latitude")
plt.show()
