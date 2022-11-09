import logging
import os
from typing import Callable, Optional, Coroutine

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from common import try_load_dotenv, PayloadMessage
from common.contants import TOPICS

BotCallback = Callable[[str, PayloadMessage], Coroutine]
_callback_inner: Optional[BotCallback] = None


try_load_dotenv()
bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
dp = Dispatcher(bot)


def set_async_callback(callback: BotCallback) -> None:
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
    await _callback(TOPICS.SUM, message, nums)


@dp.message_handler(commands=['product'])
async def _on_product_command(message: types.Message):
    logging.info(f'cmd from {message.chat.id}: {message.text}')

    nums = list(map(int, message.text.split()[1:]))
    await _callback(TOPICS.PRODUCT, message, nums)


@dp.message_handler(commands=['grayscale'], commands_ignore_caption=False, content_types=ContentType.PHOTO)
async def _on_grayscale_command(message: types.Message):
    logging.info(f'cmd from {message.chat.id}: {message.text}')
    await _callback(TOPICS.GRAYSCALE, message, await message.photo[-1].get_url())


async def on_result(msg: PayloadMessage) -> None:
    logging.info(f"replying to {msg['chat_id']}: {msg['payload']}")
    await bot.send_message(
        msg['chat_id'],
        str(msg['payload']),
        reply_to_message_id=msg['message_id']
    )


async def run() -> None:
    await dp.start_polling()
