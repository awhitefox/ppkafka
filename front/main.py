import logging
import asyncio

from consumer import TelegramConsumer
from producer import TelegramProducer
from bot import bot_init, bot_run, dp

logging.basicConfig(level=logging.INFO)

in_queue = asyncio.Queue()
out_queue = asyncio.Queue()

loop = asyncio.new_event_loop()
loop.create_task(TelegramProducer(loop).run(in_queue))
loop.create_task(TelegramConsumer(loop).run(out_queue))
bot_init(in_queue, out_queue)
loop.create_task(bot_run())
loop.run_forever()
