"""
Admin panel: faqat config.py dagi ADMIN_ID uchun ishlaydi.

Funksiyalar:
- 📢 E'lon berish (barcha foydalanuvchilarga broadcast)
- 📊 Statistika
- 📁 APK qo'shish / ro'yxatini ko'rish / o'chirish
- Forward qilingan xabarga Reply qilib, foydalanuvchiga javob yuborish
"""
import asyncio
import os

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

from config import ADMIN_ID, APK_DIR
import database as db

router = Router()
router.message.filter(F.from_user.id == ADMIN_ID)


class AdminStates(StatesGroup):
    waiting_broadcast = State()
    waiting_apk_name = State()
    waiting_apk_file = State()


def admin_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📢 E'lon berish")],
            [KeyboardButton(text="📁 APK qo'shish"), KeyboardButton(text="📋 APK ro'yxati")],
            [KeyboardButton(text="📊 Statistika")],
        ],
        resize_keyboard=True,
    )


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    await message.answer("🔐 <b>Admin panel</b>", reply_markup=admin_menu_keyboard())


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi.", reply_markup=admin_menu_keyboard())


# ---------- Statistika ----------
@router.message(F.text == "📊 Statistika")
async def show_stats(message: Message):
    count = db.get_user_count()
    apk_count = len(db.get_all_apks())
    await message.answer(
        f"📊 <b>Statistika</b>\n\n"
        f"👥 Foydalanuvchilar soni: <b>{count}</b>\n"
        f"📁 APK fayllar soni: <b>{apk_count}</b>"
    )


# ---------- E'lon berish (broadcast) ----------
@router.message(F.text == "📢 E'lon berish")
async def start_broadcast(message: Message, state: FSMContext):
    await state.set_state(AdminStates.waiting_broadcast)
    await message.answer(
        "E'lon matnini yuboring (rasm/video bilan ham bo'lishi mumkin).\n"
        "Bekor qilish uchun /cancel yozing.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(AdminStates.waiting_broadcast)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user_ids = db.get_all_user_ids()
    sent, failed = 0, 0

    status = await message.answer(f"⏳ Yuborilmoqda... (0/{len(user_ids)})")

    for i, user_id in enumerate(user_ids, start=1):
        try:
            await message.copy_to(user_id)
            sent += 1
        except Exception:
            failed += 1
        if i % 20 == 0:
            await status.edit_text(f"⏳ Yuborilmoqda... ({i}/{len(user_ids)})")
        await asyncio.sleep(0.05)  # Telegram limitidan chiqib ketmaslik uchun

    await status.edit_text(
        f"✅ E'lon yuborildi!\n\n✔️ Muvaffaqiyatli: {sent}\n❌ Xato: {failed}"
    )
    await message.answer("🔐 Admin panel", reply_markup=admin_menu_keyboard())


# ---------- APK qo'shish ----------
@router.message(F.text == "📁 APK qo'shish")
async def start_add_apk(message: Message, state: FSMContext):
    await state.set_state(AdminStates.waiting_apk_name)
    await message.answer(
        "APK uchun nom kiriting (masalan: <i>Granny 1</i>, <i>Granny 2 - Yangi versiya</i>).\n"
        "Bekor qilish uchun /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(AdminStates.waiting_apk_name)
async def process_apk_name(message: Message, state: FSMContext):
    await state.update_data(apk_name=message.text)
    await state.set_state(AdminStates.waiting_apk_file)
    await message.answer("Endi APK faylni yuboring (.apk hujjat sifatida).")


@router.message(AdminStates.waiting_apk_file, F.document)
async def process_apk_file(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    apk_name = data.get("apk_name", "APK")

    document = message.document
    if not document.file_name.lower().endswith(".apk"):
        await message.answer("⚠️ Bu .apk fayl emas. Iltimos, to'g'ri faylni yuboring yoki /cancel bosing.")
        return

    file_path = os.path.join(APK_DIR, f"{document.file_unique_id}_{document.file_name}")
    await bot.download(document, destination=file_path)

    db.add_apk(apk_name, file_path, telegram_file_id=document.file_id)
    await state.clear()
    await message.answer(f"✅ \"{apk_name}\" muvaffaqiyatli qo'shildi!", reply_markup=admin_menu_keyboard())


@router.message(AdminStates.waiting_apk_file)
async def process_apk_file_wrong_type(message: Message):
    await message.answer("⚠️ Iltimos, APK faylni <b>hujjat (document)</b> sifatida yuboring.")


# ---------- APK ro'yxati / o'chirish ----------
@router.message(F.text == "📋 APK ro'yxati")
async def list_apks(message: Message):
    apks = db.get_all_apks()
    if not apks:
        await message.answer("Hozircha APK fayllar mavjud emas.")
        return

    for apk in apks:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"del_apk_{apk['id']}")]
        ])
        await message.answer(f"📦 {apk['name']}", reply_markup=kb)


@router.callback_query(F.data.startswith("del_apk_"), F.from_user.id == ADMIN_ID)
async def delete_apk_cb(callback):
    apk_id = int(callback.data.replace("del_apk_", ""))
    apk = db.get_apk_by_id(apk_id)
    if apk:
        try:
            os.remove(apk["file_path"])
        except OSError:
            pass
        db.delete_apk(apk_id)
        await callback.message.edit_text(f"🗑 \"{apk['name']}\" o'chirildi.")
    await callback.answer()


# ---------- Foydalanuvchiga javob (Reply orqali) ----------
@router.message(F.reply_to_message)
async def reply_to_user(message: Message, bot: Bot):
    """
    Admin forward qilingan xabarga Reply qilsa, javob avtomatik
    o'sha foydalanuvchiga yuboriladi.
    """
    original_id = message.reply_to_message.message_id
    user_id = db.get_user_from_message(original_id)

    if not user_id:
        await message.answer("⚠️ Bu xabar kimga tegishli ekanini aniqlab bo'lmadi.")
        return

    try:
        await message.copy_to(user_id)
        await message.answer("✅ Javob yuborildi.")
    except Exception as e:
        await message.answer(f"❌ Yuborib bo'lmadi: {e}")
