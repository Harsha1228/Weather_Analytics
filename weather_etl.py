import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# USER INPUT

city = input("Enter City Name: ")

# OPENWEATHER API

API_KEY = "YOUR_APIKEY"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()


# ERROR HANDLING

if "main" not in data:
    print("Error:", data)
    exit()

# EXTRACT WEATHER DATA

temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]
weather_condition = data["weather"][0]["main"]


# DISPLAY TO USER

print("\nWeather Details")
print("----------------------------")
print("City:", city)
print("Temperature:", temperature, "°C")
print("Humidity:", humidity, "%")
print("Wind Speed:", wind_speed, "m/s")
print("Condition:", weather_condition)


# DATAFRAME

weather_df = pd.DataFrame({
    "city": [city],
    "temperature": [temperature],
    "humidity": [humidity],
    "wind_speed": [wind_speed],
    "weather_condition": [weather_condition],
    "recorded_at": [datetime.now()]
})


# POSTGRESQL CONNECTION

engine = create_engine(
    "postgresql://postgres:{DB_PASSWORD}@localhost:5432/weather_analytics"
)

# LOAD DATA

weather_df.to_sql(
    "weather_data",
    engine,
    if_exists="append",
    index=False
)

print("\nWeather data inserted successfully!")