import asyncio

from . import bot
from common import setup_logging, PayloadProducer, PayloadConsumer

setup_logging('bot')


loop = asyncio.new_event_loop()
try:
    prod = PayloadProducer(loop)
    cons = PayloadConsumer(loop, 'results')

    bot.set_async_callback(prod.produce)
    cons.set_async_callback(bot.on_result)

    loop.run_until_complete(asyncio.gather(
        loop.create_task(prod.start()),
        loop.create_task(cons.run()),
        loop.create_task(bot.run())
    ))
finally:
    loop.close()
