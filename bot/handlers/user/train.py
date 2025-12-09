from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import html

from bot.keyboards.train_keyboard import keyboard, result_keyboard
from bot.utils.train import send_problem_message

router = Router()

@router.message(Command('train'))
async def train(message: Message):
    await message.answer("Выбери уровень сложности задачи", reply_markup=keyboard)

@router.callback_query(F.data == 'train_medium')
async def train_medium(callback: CallbackQuery, db, **_):
    problem = await db.get_random_problem_by_difficulty("medium", callback.from_user.id)
    if problem is None:
        await callback.message.answer("Пока нет задач этой сложности 🙁")
        await callback.answer()
        return
    text = send_problem_message(problem, html.escape)
    internal_user_id = await db.get_or_create_user_id(callback.from_user.id)
    await db.mark_problem_shown(user_id=internal_user_id, problem_id=problem["id"])
    await callback.message.answer(text, parse_mode="HTML", reply_markup=result_keyboard(problem["id"]))

@router.callback_query(F.data == 'train_easy')
async def train_easy(callback: CallbackQuery, db, **_):
    problem = await db.get_random_problem_by_difficulty("easy", callback.from_user.id)
    if problem is None:
        await callback.message.answer("Пока нет задач этой сложности 🙁")
        await callback.answer()
        return
    text = send_problem_message(problem, html.escape)
    internal_user_id = await db.get_or_create_user_id(callback.from_user.id)
    await db.mark_problem_shown(user_id=internal_user_id, problem_id=problem["id"])
    await callback.message.answer(text, parse_mode="HTML", reply_markup=result_keyboard(problem["id"]))

@router.callback_query(F.data == 'train_hard')
async def train_hard(callback: CallbackQuery, db, **_):
    problem = await db.get_random_problem_by_difficulty("hard", callback.from_user.id)
    if problem is None:
        await callback.message.answer("Пока нет задач этой сложности 🙁")
        await callback.answer()
        return
    text = send_problem_message(problem, html.escape)
    internal_user_id = await db.get_or_create_user_id(callback.from_user.id)
    await db.mark_problem_shown(user_id=internal_user_id, problem_id=problem["id"])
    await callback.message.answer(text, parse_mode="HTML", reply_markup=result_keyboard(problem["id"]))

@router.callback_query(F.data.startswith("solved:"))
async def solved_train(callback: CallbackQuery, db, **_):
    _, problem_id_str = callback.data.split(':')
    problem_id = int(problem_id_str)
    internal_user_id = await db.get_or_create_user_id(callback.from_user.id)
    await db.mark_problem_solved(user_id=internal_user_id, problem_id=problem_id)
    await callback.answer("Отметил задачу как решённую ✅")
    await callback.message.answer("Можешь взять следующую задачу командой /train")
