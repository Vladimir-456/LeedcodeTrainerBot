from aiogram import Router

from bot.handlers.user import user_router

main_router = Router()
main_router.include_router(user_router)