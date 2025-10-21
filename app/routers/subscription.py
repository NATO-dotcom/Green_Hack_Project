from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..services.sms_service import send_sms
from ..services.weather_service import get_weather, generate_recommendation

router = APIRouter(prefix="/api", tags=["Subscription"])

@router.post("/subscribe", response_model=schemas.SubscriptionResponse)
def subscribe(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(models.User).filter(models.User.phone_number == subscription.phone_number).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already subscribed")

        new_user = crud.create_user(db, subscription)

        # Fetch weather & AI recommendation
        weather_data = get_weather(subscription.location)
        recommendation = generate_recommendation(weather_data)

        sms_message = (
            f"Welcome to WeatherWise!\n"
            f"You’re subscribed for {subscription.location} alerts.\n\n"
            f"AI Tip: {recommendation}"
        )
        sms_response = send_sms(subscription.phone_number, sms_message)

        return {"message": "Subscription successful", "sms_response": sms_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
