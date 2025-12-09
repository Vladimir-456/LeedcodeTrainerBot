from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command('stats'))
async def stats_handler(message: Message, db, **_):
    stats = await db.get_user_stats(message.from_user.id)

    if not stats:
        await message.answer("Пока нет статистики по задачам 🙃")
        return

    lines = ["<b>Твоя статистика по задачам:</b>\n"]
    for row in stats:
        diff = row["difficulty"].capitalize()
        shown = row["shown_count"]
        solved = row["solved_count"]
        percent = int(solved * 100 / shown) if shown else 0
        lines.append(
            f"• <b>{diff}</b>: {solved}/{shown} решено ({percent}%)"
        )

    text = "\n".join(lines)
    await message.answer(text, parse_mode="HTML")

