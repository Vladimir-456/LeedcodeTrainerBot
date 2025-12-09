from aiogram import Router

from . import start, register_db, train, stats, help


user_router = Router()

user_router.include_router(start.router)
user_router.include_router(register_db.router)
user_router.include_router(train.router)
user_router.include_router(stats.router)
user_router.include_router(help.router)