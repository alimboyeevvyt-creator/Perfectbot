# PERFECT — Telegram bot

## 🔧 Imkoniyatlar

- 💬 Foydalanuvchi botga yozgan xabarlari avtomatik adminga (sizga) yetkaziladi, siz esa oddiygina **Reply** qilib javob berasiz
- 🔐 Alohida **admin panel** (`/admin` buyrug'i, faqat sizning ID'ingiz uchun ochiladi)
- 📢 Admin paneldan barcha foydalanuvchilarga **e'lon (broadcast)** yuborish
- 🚫 Guruhda **link va fayl yuborishni** avtomatik taqiqlash (adminlar bundan mustasno)
- 🎬 Foydalanuvchi link yuborsa (YouTube/Instagram/TikTok va h.k.), bot videoni **yuklab beradi**
- 📁 Admin turli **APK fayllarni** (masalan, Granny 1, Granny 2...) botga yuklab qo'yadi, foydalanuvchilar esa menyu orqali tanlab yuklab olishadi

## 📦 O'rnatish

1. Python 3.10+ o'rnatilgan bo'lishi kerak

2. Loyihani yuklab, papkaga kiring, so'ng kerakli kutubxonalarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```

3. `.env.example` faylidan nusxa oling va `.env` deb nomlang:
   ```bash
   cp .env.example .env
   ```

4. `.env` faylini oching va quyidagilarni to'ldiring:
   - **BOT_TOKEN** — [@BotFather](https://t.me/BotFather) orqali yaratilgan bot tokeni
   - **ADMIN_ID** — sizning shaxsiy Telegram ID'ingiz ([@userinfobot](https://t.me/userinfobot) orqali bilib olishingiz mumkin)

5. Botni ishga tushiring:
   ```bash
   python bot.py
   ```

## 🖥 Admin paneldan foydalanish

Botga shaxsiy (private) chatda `/admin` deb yozing — quyidagi tugmalar chiqadi:

| Tugma | Vazifasi |
|---|---|
| 📢 E'lon berish | Barcha foydalanuvchilarga xabar (matn/rasm/video) yuborish |
| 📁 APK qo'shish | Yangi APK fayl yuklash (nom + fayl) |
| 📋 APK ro'yxati | Mavjud APK fayllarni ko'rish va o'chirish |
| 📊 Statistika | Foydalanuvchilar va APK fayllar soni |

**Foydalanuvchiga javob berish:** Foydalanuvchi yozgan xabar sizga forward qilinganda, o'sha xabarga oddiy **Reply** qiling — javobingiz avtomatik unga yetib boradi.

## 🤖 Botni guruhga qo'shish

1. Botni guruhingizga a'zo qiling
2. Botga **admin** huquqini bering (xabarlarni o'chira olishi uchun "Delete messages" ruxsati kerak)
3. Shundan so'ng guruhda link yoki fayl yuborilsa, bot avtomatik o'chiradi (guruh adminlaridan tashqari)

## 📁 Loyiha tuzilishi

```
perfect_bot/
├── bot.py              # Botni ishga tushiruvchi asosiy fayl
├── config.py           # Sozlamalar (token, admin ID, papkalar)
├── database.py         # SQLite ma'lumotlar bazasi funksiyalari
├── handlers/
│   ├── user.py         # Oddiy foydalanuvchi bilan ishlash
│   ├── admin.py        # Admin panel
│   ├── group.py        # Guruh moderatsiyasi
│   └── downloader.py   # Video yuklab olish (yt-dlp)
├── apk_files/           # Yuklangan APK fayllar shu yerda saqlanadi
├── downloads/            # Video yuklab olish uchun vaqtinchalik papka
├── requirements.txt
├── .env.example
└── README.md
```

## ⚠️ Eslatmalar

- Telegram Bot API orqali bot yubora oladigan fayl hajmi standart holatda **~50MB** bilan cheklangan (`config.py` dagi `MAX_FILE_SIZE_MB`). Kattaroq fayllar/videolar uchun Telegram Bot API Local Server kerak bo'ladi.
- Video yuklab berish funksiyasi ba'zi platformalarda (Instagram, TikTok) login/cookie talab qilishi mumkin — agar xatolik chiqsa, `yt-dlp` sozlamalarini kengaytirish kerak bo'lishi mumkin.
- Bot doim ishlab turishi uchun uni server (VPS) da yoki `systemd`/`screen`/`pm2` kabi vositalar bilan fon jarayon sifatida ishga tushirish tavsiya etiladi.
