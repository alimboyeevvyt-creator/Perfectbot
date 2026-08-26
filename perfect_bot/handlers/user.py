"""
Oddiy foydalanuvchilar bilan ishlaydigan handlerlar:
- /start
- APK fayllar menyusi
- Video link yuborilsa -> yuklab berish
- Oddiy matn yozilsa -> adminga forward qilish
"""
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from config import ADMIN_ID
import database as db
from handlers.downloader import extract_url, download_video, cleanup_file

router = Router()


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 APK fayllar", callback_data="show_apks")],
        [InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help")],
    ])


@router.message(CommandStart())
async def cmd_start(message: Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "<b>PERFECT</b> botiga xush kelibsiz.\n\n"
        "• 📁 APK fayllarni yuklab olishingiz mumkin\n"
        "• 🔗 Video link yuborsangiz, men uni yuklab beraman\n"
        "• ✍️ Savolingiz bo'lsa, shunchaki yozing — men adminga yetkazaman",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == "help")
async def cb_help(callback):
    await callback.message.answer(
        "ℹ️ <b>Botdan qanday foydalanish:</b>\n\n"
        "1️⃣ APK fayl olish uchun \"📁 APK fayllar\" tugmasini bosing\n"
        "2️⃣ Video yuklab olish uchun link yuboring (YouTube/Instagram/TikTok)\n"
        "3️⃣ Admin bilan bog'lanish uchun shunchaki xabar yozing"
    )
    await callback.answer()


@router.callback_query(F.data == "show_apks")
async def cb_show_apks(callback):
    apks = db.get_all_apks()
    if not apks:
        await callback.message.answer("Hozircha APK fayllar mavjud emas.")
        await callback.answer()
        return

    buttons = [
        [InlineKeyboardButton(text=apk["name"], callback_data=f"get_apk_{apk['id']}")]
        for apk in apks
    ]
    await callback.message.answer(
        "📁 Mavjud APK fayllar:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("get_apk_"))
async def cb_get_apk(callback, bot: Bot):
    apk_id = int(callback.data.replace("get_apk_", ""))
    apk = db.get_apk_by_id(apk_id)
    if not apk:
        await callback.answer("Fayl topilmadi.", show_alert=True)
        return

    await callback.answer("Yuklanmoqda...")
    if apk["telegram_file_id"]:
        # Telegram'da avval yuklangan fayl_id bo'yicha tezroq yuborish
        await bot.send_document(callback.from_user.id, apk["telegram_file_id"], caption=apk["name"])
    else:
        await bot.send_document(callback.from_user.id, FSInputFile(apk["file_path"]), caption=apk["name"])


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
    if message.from_user.id == ADMIN_ID:
        return  # adminning o'zi yozsa, boshqa handler ishlaydi

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
