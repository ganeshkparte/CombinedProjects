# weather_utils.py

import requests
import csv
from config import API_KEY, BASE_URL


def fetch_forecast(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data for {city}: {e}")
        return None


def extract_relevant_data(forecast_json):
    forecast_list = forecast_json.get("list", [])
    extracted_data = []
    for entry in forecast_list:
        data_point = {
            "date": entry["dt_txt"],
            "temp": entry["main"]["temp"],
            "humidity": entry["main"]["humidity"],
            "condition": entry["weather"][0]["main"].lower(),
        }
        extracted_data.append(data_point)
    return extracted_data


def save_forecast_to_csv(city, data):
    filename = f"{city.lower()}_forecast.csv".replace(" ", "_")
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "temp", "humidity", "condition"])
        writer.writeheader()
        writer.writerows(data)


def generate_alerts(city, data):
    alerts = []
    for entry in data:
        date = entry["date"]
        temp = entry["temp"]
        condition = entry["condition"]
        if temp > 35:
            alerts.append(f"High Temperature Alert in {city} on {date}")
        if temp < 5:
            alerts.append(f"Cold Weather Alert in {city} on {date}")
        if "rain" in condition or "storm" in condition:
            alerts.append(f"Storm/Rain Alert in {city} on {date}")
    return alerts
