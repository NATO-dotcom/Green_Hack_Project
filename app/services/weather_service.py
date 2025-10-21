import requests, os, google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API = os.getenv("WEATHER_API_KEY")
GEMINI_API = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API)

def get_weather(location: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch weather data"}
    return response.json()

def generate_recommendation(weather_data):
    try:
        model = genai.GenerativeModel("gemini-pro")
        description = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        city = weather_data["name"]

        prompt = f"""
        Current weather in {city}: {description}, temperature {temp}°C.
        Give useful recommendations for farmers and business owners to stay safe or productive.
        """
        result = model.generate_content(prompt)
        return result.text
    except Exception as e:
        return f"AI recommendation unavailable: {str(e)}"

