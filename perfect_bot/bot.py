"""
PERFECT bot - asosiy ishga tushirish fayli.

Ishga tushirish:
    python bot.py
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from config import BOT_TOKEN, ADMIN_ID
from database import init_db
from handlers import group, admin, user

logging.basicConfig(level=logging.INFO)


async def setup_commands(bot: Bot):
    # Barcha foydalanuvchilar uchun ko'rinadigan buyruqlar
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Botni ishga tushirish"),
            BotCommand(command="myid", description="Telegram ID'imni bilish"),
        ],
        scope=BotCommandScopeDefault(),
    )

    # Faqat admin uchun qo'shimcha buyruq
    if ADMIN_ID:
        try:
            await bot.set_my_commands(
                [
                    BotCommand(command="start", description="Botni ishga tushirish"),
                    BotCommand(command="admin", description="🔐 Admin panel"),
                    BotCommand(command="myid", description="Telegram ID'imni bilish"),
                    BotCommand(command="cancel", description="Amalni bekor qilish"),
                ],
                scope=BotCommandScopeChat(chat_id=ADMIN_ID),
            )
        except Exception as e:
            logging.warning(f"Admin uchun buyruqlar o'rnatilmadi (avval botga /start bosing): {e}")


async def main():
    if not BOT_TOKEN or BOT_TOKEN == "BOT_TOKEN_BU_YERGA":
        raise RuntimeError(
            "BOT_TOKEN sozlanmagan! .env faylida BOT_TOKEN=... deb yozing."
        )

    init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Tartib muhim: avval guruh moderatsiyasi, keyin admin, so'ng oddiy foydalanuvchi
    dp.include_router(group.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)

    logging.info("PERFECT bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
