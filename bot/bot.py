import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from .handlers import main_router
from .db.database import Database

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(TOKEN)

dp = Dispatcher()
dp.include_router(main_router)
db = Database()

async def main():
    logging.basicConfig(level=logging.INFO)
    await db.connect()
    await db.create_table()

    dp['db'] = db
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
