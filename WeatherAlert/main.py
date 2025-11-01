
import requests
import pandas as pd

API_KEY = "881fad6b0866f7fae7e57fddbe94dbbb"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
CITIES = ["London", "New York", "Delhi", "Tokyo"]

for city in CITIES:
    print(f"📍 Fetching data for {city}...")
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200 and "list" in data:
        forecast_list = data["list"]
        rows = []

        for forecast in forecast_list:
            row = {
                "Date": forecast["dt_txt"],
                "Temperature (°C)": forecast["main"]["temp"],
                "Weather": forecast["weather"][0]["description"],
                "Humidity (%)": forecast["main"]["humidity"],
                "Wind Speed (m/s)": forecast["wind"]["speed"]
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        filename = city.replace(" ", "_") + "_forecast.xlsx"
        df.to_excel(filename, index=False)
        print(f"✅ Saved forecast for {city} in {filename}\n")
    else:
        print(f"❌ Failed to fetch data for {city}: {data.get('message', 'Unknown error')}")
