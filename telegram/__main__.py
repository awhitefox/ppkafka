import os
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from telegram import bot  # noqa: E402
from common import setup_logging, PayloadProducer, PayloadConsumer  # noqa: E402
from common.contants import TOPICS  # noqa: E402

setup_logging('bot')


loop = asyncio.new_event_loop()
try:
    prod = PayloadProducer(loop)
    cons = PayloadConsumer(loop, TOPICS.RESULTS)

    bot.set_async_callback(prod.produce)
    cons.set_async_callback(bot.on_result)

    loop.run_until_complete(asyncio.gather(
        loop.create_task(prod.start()),
        loop.create_task(cons.run()),
        loop.create_task(bot.run())
    ))
finally:
    loop.close()
