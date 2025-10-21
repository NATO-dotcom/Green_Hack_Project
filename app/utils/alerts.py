from typing import List, Tuple

class AlertRule:
    @staticmethod
    def analyze(data: dict) -> Tuple[List[dict], List[str]]:
        alerts, recs = [], []
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rain = data.get("rain", {}).get("1h", 0)
        wind = data["wind"]["speed"]

        if rain > 10:
            alerts.append({"type": "heavy_rain", "message": "🌧️ Heavy rainfall expected"})
            recs += ["Cover harvested crops", "Avoid travel if possible"]
        elif 2 < rain <= 10:
            alerts.append({"type": "moderate_rain", "message": "🌦️ Moderate rain - good for crops"})
            recs += ["Ideal for planting"]

        if temp > 35:
            alerts.append({"type": "heatwave", "message": "🔥 High temperature"})
            recs += ["Water crops early morning", "Provide livestock shade"]

        if wind > 10:
            alerts.append({"type": "wind_alert", "message": "💨 Strong winds expected"})
            recs += ["Secure structures"]

        if 20 <= temp <= 28 and 40 <= humidity <= 70:
            alerts.append({"type": "ideal", "message": "✅ Ideal conditions for farming"})
            recs += ["Perfect day for planting or harvesting"]

        return alerts, recs
