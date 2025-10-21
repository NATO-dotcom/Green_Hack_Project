def send_sms(phone_number: str, message: str):
    print(f"Sending SMS to {phone_number}: {message}")
    return {"status": "success", "phone_number": phone_number, "message": message}

