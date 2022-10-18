import json
import logging
from typing import Callable

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


async def main_loop(consumer_topic: str, producer_topic: str, payload_handler: Callable):
    consumer = AIOKafkaConsumer(
        consumer_topic,
        bootstrap_servers='localhost:9092',
        enable_auto_commit=True
    )
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
    )
    try:
        await consumer.start()
        await producer.start()
        while True:
            rec = await consumer.getone()
            data = json.loads(rec.value.decode('utf-8'))

            logging.info(f'handling request from {data["chat_id"]}: {data["payload"]}')

            data['payload'] = payload_handler(data['payload'])
            await producer.send_and_wait(producer_topic, json.dumps(data).encode('utf-8'))
    finally:
        await consumer.stop()
        await producer.stop()
