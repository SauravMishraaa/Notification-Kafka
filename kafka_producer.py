from aiokafka import AIOKafkaProducer
import json
import asyncio

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = "notifications"


async def init_producer():
    return AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

async def send_notification(data: dict):
    producer = await init_producer()
    await producer.start()
    try:
        await producer.send_and_wait(TOPIC, data)
    finally:
        await producer.stop()