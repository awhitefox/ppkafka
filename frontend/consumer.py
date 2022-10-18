import json
import logging
from typing import Callable, Awaitable

from aiokafka import AIOKafkaConsumer


class TelegramConsumer:
    def __init__(self, loop):
        self._consumer = AIOKafkaConsumer(
            'results',
            loop=loop,
            bootstrap_servers='localhost:9092',
            enable_auto_commit=True
        )
        self._callback = None

    async def run(self):
        await self._consumer.start()
        try:
            while True:
                rec = await self._consumer.getone()
                data = json.loads(rec.value.decode('utf-8'))
                if self._callback is None:
                    logging.warning('consumer has no callback function set')
                    continue
                await self._callback(
                    data['chat_id'],
                    data['message_id'],
                    data['payload']
                )
        finally:
            await self._consumer.stop()

    def set_async_callback(self, callback: Callable[[int, int, ...], Awaitable]):
        self._callback = callback
