import asyncio
import json

from aiokafka import AIOKafkaProducer


class TelegramProducer:
    def __init__(self, loop):
        self._producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers='localhost:9092',
        )

    async def run(self, in_queue: asyncio.Queue):
        await self._producer.start()
        try:
            while True:
                topic, chat_id, message_id, payload = await in_queue.get()
                data = {
                    'chat_id': chat_id,
                    'message_id': message_id,
                    'payload': payload
                }
                await self._producer.send_and_wait(topic, json.dumps(data).encode('utf-8'))
        finally:
            await self._producer.stop()
