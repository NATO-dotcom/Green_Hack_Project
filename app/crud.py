from . import models

def create_user(db, subscription):
    new_user = models.User(
        phone_number=subscription.phone_number,
        location=subscription.location,
        language=subscription.language,
        alert_types=subscription.alert_types
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

