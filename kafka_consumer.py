from aiokafka import AIOKafkaConsumer
import asyncio
import json

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = "notifications"

async def deliver(data):
    print(f"[deliver] -> user: {data['user_id']} | type: {data['type']} | msg: \"{data['message']}\"")

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id="notification-handler"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await deliver(msg.value)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())