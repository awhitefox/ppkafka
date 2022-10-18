import logging
from typing import Callable, Awaitable, Optional

from aiogram import Bot, Dispatcher, types


with open('../token') as t_file:
    bot = Bot(token=t_file.read())
    dp = Dispatcher(bot)

_callback_inner: Optional[Callable[[str, int, int, ...], Awaitable]] = None


def set_async_callback(callback: Callable[[str, int, int, ...], Awaitable]):
    global _callback_inner
    _callback_inner = callback


async def _callback(topic: str, c_id: int, m_id: int, payload) -> None:
    if _callback_inner is None:
        logging.warning('bot has no callback function set')
        return
    await _callback_inner(topic, c_id, m_id, payload)


@dp.message_handler(commands=['start', 'help'])
async def on_sum_command(message: types.Message):
    await message.answer('\n'.join((
        '/sum [x1] [x2] ... [xn]',
        '/product [x1] [x2] ... [xn]'
    )))


@dp.message_handler(commands=['sum'])
async def on_sum_command(message: types.Message):
    logging.info(f'cmd from {message.chat.id}: {message.text}')

    nums = list(map(int, message.text.split()[1:]))
    await _callback('sum', message.chat.id, message.message_id, nums)


@dp.message_handler(commands=['product'])
async def on_product_command(message: types.Message):
    logging.info(f'cmd from {message.chat.id}: {message.text}')

    nums = list(map(int, message.text.split()[1:]))
    await _callback('product', message.chat.id, message.message_id, nums)


async def on_result(c_id: int, m_id: int, payload) -> None:
    logging.info(f'replying to {c_id}: {payload}')
    await bot.send_message(c_id, payload, reply_to_message_id=m_id)


async def run() -> None:
    await dp.start_polling()
