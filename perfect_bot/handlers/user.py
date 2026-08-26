"""
Foydalanuvchilar bilan ishlaydigan handlerlar:
- /start (bot o'zini va funksiyalarini tanishtiradi)
- /myid
- Tugmali menyu: video yuklab olish, bot buyurtma qilish
- Video link yuborilsa -> yuklab berish
- Oddiy matn yozilsa -> adminga forward qilish
"""
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, FSInputFile,
)

from config import ADMIN_ID, ADMIN_USERNAME
import database as db
from handlers.downloader import extract_url, download_video, cleanup_file

router = Router()

BTN_VIDEO = "🎬 Video yuklab olish"
BTN_ORDER_BOT = "📞 Bot buyurtma qilish"
BTN_HELP = "ℹ️ Yordam"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_VIDEO)],
            [KeyboardButton(text=BTN_ORDER_BOT), KeyboardButton(text=BTN_HELP)],
        ],
        resize_keyboard=True,
    )


def contact_admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ @" + ADMIN_USERNAME + " bilan bog'lanish",
                               url=f"https://t.me/{ADMIN_USERNAME}")]
    ])


WELCOME_TEXT = (
    "Assalomu alaykum! Men <b>PERFECT</b> botiman 🤖\n\n"
    "Men nimalarni qila olaman:\n\n"
    "🎬 <b>Video yuklab berish</b> — Instagram yoki YouTube linkini yuboring, "
    "men videoni yuklab, shu yerga tashlab beraman\n\n"
    "📞 <b>Bot buyurtma qilish</b> — o'zingizga shunga o'xshash bot "
    "kerak bo'lsa, ishlab chiquvchi bilan bog'lanishingiz mumkin\n\n"
    "✍️ Shuningdek, menga xabar yozsangiz, u to'g'ridan-to'g'ri adminga yetkaziladi\n\n"
    "Pastdagi tugmalardan foydalaning 👇"
)


@router.message(Command("myid"))
async def cmd_myid(message: Message):
    await message.answer(f"🆔 Sizning ID'ingiz: <code>{message.from_user.id}</code>")


@router.message(CommandStart())
async def cmd_start(message: Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_HELP)
async def btn_help(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_ORDER_BOT)
async def btn_order_bot(message: Message):
    await message.answer(
        "🤖 O'zingizga shunga o'xshash bot kerakmi?\n\n"
        "Buyurtma berish uchun quyidagi tugma orqali bog'laning:",
        reply_markup=contact_admin_keyboard(),
    )


@router.message(F.text == BTN_VIDEO)
async def btn_video(message: Message):
    await message.answer(
        "🎬 Instagram yoki YouTube video linkini shu yerga yuboring — "
        "men uni yuklab, sizga jo'nataman."
    )


@router.message(F.text.regexp(r"https?://").as_("_"))
async def handle_video_link(message: Message, bot: Bot):
    url = extract_url(message.text)
    if not url:
        return

    status_msg = await message.answer("⏳ Video yuklanmoqda, biroz kuting...")
    file_path, error = download_video(url)

    if error:
        await status_msg.edit_text(f"❌ {error}")
        return

    try:
        await message.answer_video(FSInputFile(file_path), caption="✅ Video tayyor!")
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ Videoni yuborib bo'lmadi: {e}")
    finally:
        cleanup_file(file_path)


@router.message(F.chat.type == "private")
async def forward_to_admin(message: Message, bot: Bot):
    """Foydalanuvchi yozgan har qanday boshqa xabarni adminga forward qiladi."""
    if not ADMIN_ID or message.from_user.id == ADMIN_ID:
        return

    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)

    info_text = (
        f"✉️ <b>Yangi xabar</b>\n"
        f"👤 {message.from_user.first_name} "
        f"(@{message.from_user.username or 'yoq'})\n"
        f"🆔 <code>{message.from_user.id}</code>\n\n"
        f"Javob berish uchun shu xabarga <b>Reply</b> qiling."
    )
    await bot.send_message(ADMIN_ID, info_text)
    forwarded = await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

    db.save_message_map(forwarded.message_id, message.from_user.id)
