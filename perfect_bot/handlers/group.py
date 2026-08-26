"""
Guruhda to'liq nazorat:
- Link yuborilsa -> xabar o'chiriladi + foydalanuvchi 5 daqiqaga yoza olmaydi (mute)
- Fayl/hujjat (shu jumladan APK) yuborilsa -> xabar o'chiriladi + 5 daqiqa mute
- Guruh adminlari bundan mustasno
"""
import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, ChatPermissions

from config import BLOCK_LINKS, BLOCK_FILES, MUTE_MINUTES

router = Router()

# Faqat guruh va superguruh chatlarida ishlaydi
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

MUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_photos=False,
    can_send_videos=False,
    can_send_video_notes=False,
    can_send_voice_notes=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
)


async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


async def mute_user(bot: Bot, chat_id: int, user_id: int):
    until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=MUTE_MINUTES)
    try:
        await bot.restrict_chat_member(
            chat_id, user_id, permissions=MUTED_PERMISSIONS, until_date=until
        )
    except Exception:
        pass  # bot admin bo'lmasa yoki huquqi yetmasa, jim o'tkazib yuboriladi


async def punish(message: Message, bot: Bot, reason: str):
    if await is_admin(bot, message.chat.id, message.from_user.id):
        return

    try:
        await message.delete()
    except Exception:
        pass

    await mute_user(bot, message.chat.id, message.from_user.id)

    try:
        await message.answer(
            f"⛔ {message.from_user.first_name}, {reason} taqiqlangan!\n"
            f"Siz {MUTE_MINUTES} daqiqaga xabar yoza olmaysiz."
        )
    except Exception:
        pass


@router.message(F.text.regexp(r"https?://|t\.me/|www\."))
async def block_links(message: Message, bot: Bot):
    if not BLOCK_LINKS:
        return
    await punish(message, bot, "guruhda link yuborish")


@router.message(F.document | F.video | F.audio)
async def block_files(message: Message, bot: Bot):
    if not BLOCK_FILES:
        return
    await punish(message, bot, "guruhda fayl yuborish")
