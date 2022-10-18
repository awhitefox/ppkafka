import logging
import asyncio

import bot
from consumer import TelegramConsumer
from producer import TelegramProducer

logging.basicConfig(level=logging.INFO)

loop = asyncio.new_event_loop()

prod = TelegramProducer(loop)
cons = TelegramConsumer(loop)

bot.set_async_callback(prod.produce)
cons.set_async_callback(bot.on_result)

loop.create_task(prod.start())
loop.create_task(cons.run())
loop.create_task(bot.run())
loop.run_forever()
