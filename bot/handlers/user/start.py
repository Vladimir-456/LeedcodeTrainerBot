from aiogram import Router, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, db, **_):
    await db.add_user(message.from_user.id, message.from_user.username)
    await message.answer("«Добро пожаловать в твой личный LeetCode‑зал. "
                         "Здесь ты будешь получать задачи по уровням сложности, отмечать решённые и смотреть свой прогресс. "
                         "Нажми /train и возьми первую задачу на сегодня.»")