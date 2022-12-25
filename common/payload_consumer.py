import json
import logging
import os
from typing import Callable, Optional, Coroutine

from aiokafka import AIOKafkaConsumer
from . import PayloadMessage

ConsumerCallback = Callable[[PayloadMessage], Coroutine]


class PayloadConsumer:
    def __init__(self, loop, topic: str):
        self._consumer = AIOKafkaConsumer(
            topic,
            loop=loop,
            group_id='default',
            bootstrap_servers=f'{os.getenv("BOOTSTRAP_SERVER")}:9092',
            enable_auto_commit=True
        )
        self._callback: Optional[ConsumerCallback] = None

    async def run(self) -> None:
        await self._consumer.start()
        try:
            while True:
                rec = await self._consumer.getone()
                data = json.loads(rec.value.decode('utf-8'))
                if self._callback is None:
                    logging.warning('consumer has no callback function set')
                    continue
                await self._callback(data)
        finally:
            await self._consumer.stop()

    def set_async_callback(self, callback: ConsumerCallback) -> None:
        self._callback = callback
