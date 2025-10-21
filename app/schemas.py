from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    phone_number: str
    location: str
    language: str
    alert_types: str

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionResponse(BaseModel):
    message: str
    sms_response: dict

