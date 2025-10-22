import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys
OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY")
GEMINI_API = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API)

# Function: Fetch real-time weather data
def get_weather(location: str):
    """Fetch current weather data from OpenWeather API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch weather data for {location}"}
    
    return response.json()


# Function: Generate AI-based recommendation (English + Kiswahili)
def generate_recommendation(weather_data, language: str = "en"):
    """Generate localized, AI-powered weather recommendations."""
    try:
        # Extract key weather details
        description = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        city = weather_data["name"]

        # Choose Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Define the localized prompt
        if language.lower() in ["sw", "kiswahili"]:
            prompt = f"""
            Hali ya hewa ya sasa katika {city}: {description}, joto ni {temp}°C.
            Toa ushauri mfupi kwa wakulima na wafanyabiashara kuhusu jinsi ya kujikinga
            au kufaidika kutokana na hali hii ya hewa. 
            Mifano:
            - "Mvua kubwa inanyesha, hakikisha mazao yako yamefunikwa vizuri."
            - "Joto kali leo, kunywa maji mengi na linda mifugo wako."
            """
        else:
            prompt = f"""
            Current weather in {city}: {description}, temperature {temp}°C.
            Give a short, practical weather safety tip or productivity recommendation
            for farmers and business owners in Kenya.
            Examples:
            - "Heavy rain expected — cover your crops and store grains safely."
            - "Sunny and dry — a good day for drying harvested crops."
            """

        # Generate AI response
        result = model.generate_content(prompt)
        tip = result.text.strip() if result.text else "AI Tip unavailable."

        return f"AI Tip: {tip}"

    except Exception as e:
        return f"AI recommendation unavailable: {str(e)}"


