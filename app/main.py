from fastapi import FastAPI
from .routers import subscription
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="WeatherWise API")

app.include_router(subscription.router)

@app.get("/")
def root():
    return {"message": "Welcome to WeatherWise! 🌦️"}


