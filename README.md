# Notification service

Lightweight example that sends notifications to a Kafka topic and consumes them with an async consumer.

**Contents**
- **Overview:** small FastAPI app that enqueues notification messages to Kafka
- **Files:** `main.py`, `kafka_producer.py`, `kafka_consumer.py`, `docker-compose.yml`

**Requirements:**
- Python 3.10+
- Install dependencies (FastAPI, aiokafka, uvicorn)

```bash
uv init
```

```bash
uv add fastapi uvicorn aiokafka
```

**Run Kafka (local, using Podman)**

- This repository includes `docker-compose.yml` that starts Zookeeper and Kafka.

```yaml
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
  kafka:
    image: confluentinc/cp-kafka:7.4.0
```

Then pull and start:

```bash
podman pull docker.io/confluentinc/cp-zookeeper:7.4.0
podman pull docker.io/confluentinc/cp-kafka:7.4.0
podman-compose up -d
```


**Run the FastAPI app**

```bash
uvicorn main:app --reload
```

POST a notification :

```bash
curl -X POST http://localhost:8000/notify/ \
  -H 'Content-Type: application/json' \
  -d '{"user_id":45,"message":"order shipped","type":"sms"}'
```

Run the consumer locally:

```bash
uv run kafka_consumer.py
```

Expected Output:
```bash
[deliver] -> user: 45 | type: sms | msg: "order shipped"
```

**Producer & Consumer**

- `kafka_producer.py` exposes `send_notification(data: dict)` — used by `main.py`.
- `kafka_consumer.py` is an async consumer that prints delivered notifications.


**Ports**
- Kafka: `9092` (mapped to host)
- Zookeeper: 2181 (container internal)

**Behind the Curtain (Why It Works)**
- FastAPI responds in ms — doesn't care what happens to the message later.
- Kafka ensures message durability (until consumed).
- Consumer is long-lived; can be restarted, scaled.

**Benefits**
- FastAPI stays fast. Delivery is async and decoupled.
- Kafka absorbs spikes. If 1000 messages suddenly come in, the system doesn't fall over.
- Retryable. If delivery fails, you can requeue.
- Observable. You can track delivered vs pending.