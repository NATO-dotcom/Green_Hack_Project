from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AlertSubscription(BaseModel):
    phone_number: str
    location: str
    language: str = "en"
    alert_types: List[str] = ["rain", "heat", "wind"]

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    humidity: int
    rainfall: float
    wind_speed: float
    description: str
    alerts: List[dict]
    recommendations: List[str]
    timestamp: datetime
