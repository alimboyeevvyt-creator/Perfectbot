"""
Guruhda tartib o'rnatish:
- Link yuborilsa -> o'chiriladi
- Fayl/hujjat yuborilsa -> o'chiriladi
- Adminlar bundan mustasno
"""
from aiogram import Router, F, Bot
from aiogram.types import Message

from config import BLOCK_LINKS, BLOCK_FILES

router = Router()

# Faqat guruh va superguruh chatlarida ishlaydi
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


@router.message(F.text.regexp(r"https?://|t\.me/|www\."))
async def block_links(message: Message, bot: Bot):
    if not BLOCK_LINKS:
        return
    if await is_admin(bot, message.chat.id, message.from_user.id):
        return
    try:
        await message.delete()
        warn = await message.answer(
            f"⚠️ {message.from_user.first_name}, guruhda link yuborish taqiqlangan!"
        )
    except Exception:
        pass


@router.message(F.document | F.video | F.audio)
async def block_files(message: Message, bot: Bot):
    if not BLOCK_FILES:
        return
    if await is_admin(bot, message.chat.id, message.from_user.id):
        return
    try:
        await message.delete()
        warn = await message.answer(
            f"⚠️ {message.from_user.first_name}, guruhda fayl yuborish taqiqlangan!"
        )
    except Exception:
        pass
