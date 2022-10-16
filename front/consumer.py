import asyncio
import json

from aiokafka import AIOKafkaConsumer


class TelegramConsumer:
    def __init__(self, loop):
        self._consumer = AIOKafkaConsumer(
            'results',
            loop=loop,
            bootstrap_servers='localhost:9092',
            enable_auto_commit=True
        )

    async def run(self, out_queue: asyncio.Queue):
        await self._consumer.start()
        try:
            while True:
                rec = await self._consumer.getone()
                data = json.loads(rec.value.decode('utf-8'))
                await out_queue.put((
                    data['chat_id'],
                    data['message_id'],
                    data['payload']
                ))
        finally:
            await self._consumer.stop()
