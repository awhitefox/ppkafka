import logging
import asyncio
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logging.basicConfig(level=logging.INFO)


async def main_loop():
    consumer = AIOKafkaConsumer(
        'product',
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

            result = 1
            for e in data['payload']:
                result *= e
            data['payload'] = result

            await producer.send_and_wait('results', json.dumps(data).encode('utf-8'))
    finally:
        await consumer.stop()
        await producer.stop()


loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main_loop())
finally:
    loop.close()
