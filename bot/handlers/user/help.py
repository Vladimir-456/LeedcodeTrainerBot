from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer('«Я помогаю тренироваться на задачах LeetCode.\nДоступные команды:\n'
                         '/start — кратко рассказывает, как работает бот/register — привязать твой LeetCode‑ник\n'
                         '/train — выбрать уровень и получить новую задачу\n'
                         '/stats — посмотреть, сколько задач ты уже решил по уровням сложности')