from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class RegisterState(StatesGroup):
    waiting_for_leetcode_username = State()

@router.message(Command('register'))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(RegisterState.waiting_for_leetcode_username)
    await message.answer("Введи свой LeetCode ник:")

@router.message(RegisterState.waiting_for_leetcode_username)
async def process_leetcode_username(
    message: Message,
    state: FSMContext,
    db, **_
):
    username = message.text.strip()
    print(message.from_user.id, username)
    await db.add_leetcode_username(message.from_user.id, username)
    await state.clear()
    await message.answer(f"Сохранил твой LeetCode ник: {username}")