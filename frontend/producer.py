import json

from aiokafka import AIOKafkaProducer


class TelegramProducer:
    def __init__(self, loop):
        self._producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers='localhost:9092',
        )

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()

    async def produce(self, topic: str, c_id: int, m_id: int, payload) -> None:
        try:
            data = {
                'chat_id': c_id,
                'message_id': m_id,
                'payload': payload
            }
            await self._producer.send_and_wait(topic, json.dumps(data).encode('utf-8'))
        except Exception as e:
            await self._producer.stop()
            raise e
