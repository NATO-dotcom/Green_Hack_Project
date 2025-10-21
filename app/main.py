from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from . import database, models, schemas
from .utils import weather_client, alerts, sms_service
import os

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="WeatherWise API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def root():
    return {"service": "WeatherWise", "status": "running"}

@app.get("/weather/{location}", response_model=schemas.WeatherResponse)
async def get_weather(location: str):
    data = await weather_client.fetch_weather(location)
    alerts_list, recs = alerts.AlertRule.analyze(data)
    return schemas.WeatherResponse(
        location=data["name"],
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        rainfall=data.get("rain", {}).get("1h", 0),
        wind_speed=data["wind"]["speed"],
        description=data["weather"][0]["description"],
        alerts=alerts_list,
        recommendations=recs,
        timestamp=datetime.now()
    )

@app.post("/subscribe")
def subscribe(sub: schemas.AlertSubscription, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.phone_number == sub.phone_number).first()
    if user:
        raise HTTPException(status_code=400, detail="User already subscribed")
    new_user = models.User(**sub.dict())
    db.add(new_user)
    db.commit()
    return {"message": f"Subscribed {sub.phone_number} for alerts in {sub.location}"}

@app.get("/subscribers")
def get_subscribers(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return {"total": len(users), "subscribers": [u.__dict__ for u in users]}
