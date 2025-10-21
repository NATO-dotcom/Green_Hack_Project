import africastalking, os
from dotenv import load_dotenv

load_dotenv()

africastalking.initialize(
    username=os.getenv("AFRICASTALKING_USERNAME"),
    api_key=os.getenv("AFRICASTALKING_API_KEY")
)
sms = africastalking.SMS

def send_sms(to: str, message: str):
    try:
        response = sms.send(message, [to])
        return {"status": "sent", "response": response}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
