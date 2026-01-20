from fastapi import FastAPI
from pydantic import BaseModel
from kafka_producer import send_notification

app = FastAPI()

class Notification(BaseModel):
    user_id: int
    message: str
    type: str

@app.post("/notify/")
async def notify(notification: Notification):
    await send_notification(notification.dict())
    return {"queued": True}