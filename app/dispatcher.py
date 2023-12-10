from aiogram import Dispatcher
from app.bot import bot
import logging
from app.handlers.quiz import router


dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
dp.include_router(router)


async def main():
    await dp.start_polling(bot)
