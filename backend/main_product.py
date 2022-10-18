import asyncio
import logging

from base import main_loop

logging.basicConfig(level=logging.INFO)


def product(payload: list[int]):
    r = 1
    for n in payload:
        r *= n
    return r


loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main_loop('product', 'results', product))
finally:
    loop.close()
