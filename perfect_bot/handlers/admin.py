"""
Admin uchun yagona funksiya: foydalanuvchidan kelgan (forward qilingan)
xabarga Reply qilib, javobni o'sha foydalanuvchiga yuborish.

Alohida "admin panel" yo'q - bu shunchaki reply orqali ishlaydigan tizim.
"""
from aiogram import Router, F, Bot
from aiogram.types import Message

from config import ADMIN_ID
import database as db

router = Router()
router.message.filter(F.from_user.id == ADMIN_ID)


@router.message(F.reply_to_message)
async def reply_to_user(message: Message, bot: Bot):
    """
    Admin forward qilingan xabarga Reply qilsa, javob avtomatik
    o'sha foydalanuvchiga yuboriladi.
    """
    original_id = message.reply_to_message.message_id
    user_id = db.get_user_from_message(original_id)

    if not user_id:
        return  # oddiy reply (bog'liq bo'lmagan) - e'tiborsiz qoldiriladi

    try:
        await message.copy_to(user_id)
        await message.answer("✅ Javob yuborildi.")
    except Exception as e:
        await message.answer(f"❌ Yuborib bo'lmadi: {e}")
