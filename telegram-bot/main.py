import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message
)

import bot as bot_module
import masstransit
import i18n
from mt_storage import MtStorage


async def main():
    rmq = await masstransit.connect_rabbitmq(
        getenv("RABBITMQ_CONNECTION"),
        contracts_namespace="Deps.Contracts",
        consume_queue="q_tg_bot",
        consume_queue_exchange="x_bot"
    )

    bot = Bot(token=getenv("TELEGRAM_TOKEN"))
    bot_module.save_static(bot)

    dp = Dispatcher(
        storage=MtStorage(rmq, 'json-store', 'json-get-request', "JsonGetResponse[]")
    )
    from router import router
    dp.include_router(router)
    i18n.setup_middleware(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
