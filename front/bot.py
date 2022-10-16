import asyncio
import logging
from asyncio import Queue
from aiogram import Bot, Dispatcher, types


with open('../token') as t_file:
    bot = Bot(token=t_file.read())
    dp = Dispatcher(bot)

_in_queue: Queue
_out_queue: Queue


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
    await _in_queue.put(('sum', message.chat.id, message.message_id, nums))


@dp.message_handler(commands=['product'])
async def on_product_command(message: types.Message):
    logging.info(f'cmd from {message.chat.id}: {message.text}')

    nums = list(map(int, message.text.split()[1:]))
    await _in_queue.put(('product', message.chat.id, message.message_id, nums))


async def _result_loop():
    while True:
        c_id, m_id, payload = await _out_queue.get()

        logging.info(f'reply for {c_id}: {payload}')

        await bot.send_message(c_id, payload, reply_to_message_id=m_id)


def bot_init(in_queue: Queue, out_queue: Queue) -> None:
    global _in_queue, _out_queue
    _in_queue = in_queue
    _out_queue = out_queue
    return dp.loop


async def bot_run() -> None:
    asyncio.create_task(_result_loop())
    await dp.start_polling()
