import asyncio
import logging
from typing import Callable

from common import PayloadMessage, PayloadProducer, PayloadConsumer


def run(consumer_topic: str, producer_topic: str, payload_handler: Callable) -> None:
    loop = asyncio.new_event_loop()
    try:
        producer = PayloadProducer(loop)
        consumer = PayloadConsumer(loop, consumer_topic)

        async def on_consume(msg: PayloadMessage) -> None:
            logging.info(f"handling request from {msg['chat_id']}: {msg['payload']}")

            msg['payload'] = payload_handler(msg['payload'])
            await producer.produce(producer_topic, msg)

        consumer.set_async_callback(on_consume)
        loop.run_until_complete(asyncio.gather(
            loop.create_task(producer.start()),
            loop.create_task(consumer.run())
        ))
    finally:
        loop.close()
