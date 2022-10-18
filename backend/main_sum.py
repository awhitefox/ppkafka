import asyncio
import logging

from base import main_loop

logging.basicConfig(level=logging.INFO)


loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main_loop('sum', 'results', sum))
finally:
    loop.close()
