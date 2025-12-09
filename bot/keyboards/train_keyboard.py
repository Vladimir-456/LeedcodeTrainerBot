from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Easy",
                callback_data="train_easy"
            ),
            InlineKeyboardButton(
                text="Medium",
                callback_data="train_medium"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Hard",
                callback_data="train_hard"
            ),
        ],
    ]
)
def result_keyboard(problem_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Решил",
                        callback_data=f"solved:{problem_id}",
                    )
                ]
            ]
        )