import json
import logging
from typing import Callable, Optional, Coroutine

from aiogram import Bot, Dispatcher, types

from common import PayloadMessage

BotCallback = Callable[[str, PayloadMessage], Coroutine]


with open('../token') as t_file:
    bot = Bot(token=t_file.read())
    dp = Dispatcher(bot)

_callback_inner: Optional[BotCallback] = None


def set_async_callback(callback: BotCallback):
    global _callback_inner
    _callback_inner = callback


async def _callback(topic: str, tg_msg: types.Message, payload) -> None:
    if _callback_inner is None:
        logging.warning('bot has no callback function set')
        return
    await _callback_inner(topic, PayloadMessage(
        chat_id=tg_msg.chat.id,
        message_id=tg_msg.message_id,
        payload=payload
    ))


@dp.message_handler(commands=['start', 'help'])
async def _on_help_command(message: types.Message):
    await message.answer('\n'.join((
        '/sum [x1] [x2] ... [xn]',
        '/product [x1] [x2] ... [xn]'
    )))


@dp.message_handler(commands=['sum'])
async def _on_sum_command(message: types.Message):
    logging.info(f'cmd from {message.chat.id}: {message.text}')

    nums = list(map(int, message.text.split()[1:]))
    await _callback('sum', message, nums)


@dp.message_handler(commands=['product'])
async def _on_product_command(message: types.Message):
    logging.info(f'cmd from {message.chat.id}: {message.text}')

    nums = list(map(int, message.text.split()[1:]))
    await _callback('product', message, nums)


async def on_result(msg: PayloadMessage) -> None:
    logging.info(f"replying to {msg['chat_id']}: {msg['payload']}")
    await bot.send_message(
        msg['chat_id'],
        json.dumps(msg['payload']),
        reply_to_message_id=msg['message_id']
    )


async def run() -> None:
    await dp.start_polling()
