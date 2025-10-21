import httpx, os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://api.openweathermap.org/data/2.5"
API_KEY = os.getenv("OPENWEATHER_API_KEY")

async def fetch_weather(location: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE_URL}/weather",
            params={"q": f"{location},KE", "appid": API_KEY, "units": "metric"},
            timeout=10.0
        )
        res.raise_for_status()
        return res.json()
