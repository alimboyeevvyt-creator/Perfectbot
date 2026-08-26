# PERFECT — Telegram bot

## 🔧 Imkoniyatlar

- 🎬 Instagram yoki YouTube link yuborilsa, bot videoni **yuklab beradi**
- 💬 Foydalanuvchi botga yozgan xabarlari avtomatik adminga yetkaziladi, admin esa **Reply** qilib javob beradi
- 🚫 Guruhda **link va fayl (shu jumladan APK) yuborish taqiqlangan** — yuborilsa xabar o'chiriladi va yuboruvchi **5 daqiqaga** guruhda yoza olmaydi (adminlar bundan mustasno)
- ⌨️ Foydalanuvchi uchun tugmali menyu (video yuklash, bot buyurtma qilish, yordam)
- 📞 "Bot buyurtma qilish" tugmasi orqali ishlab chiquvchi bilan (@Alimboyeevv) to'g'ridan-to'g'ri bog'lanish
- 👋 `/start` bosilganda bot o'zini va barcha funksiyalarini tanishtiradi

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
   - **ADMIN_ID** — sizning shaxsiy Telegram ID'ingiz (botga `/myid` deb yozib bilib olasiz)
   - **ADMIN_USERNAME** — bot buyurtma qilish tugmasida ko'rinadigan username (`@` belgisisiz, masalan `Alimboyeevv`)

5. Botni ishga tushiring:
   ```bash
   python bot.py
   ```

## 🤖 Botni guruhga qo'shish (muhim!)

Guruhda link/fayl bloklash va foydalanuvchini vaqtincha mute qilish uchun botga quyidagi huquqlar **shart**:

1. Botni guruhingizga a'zo qiling
2. Bot profiliga kirib, uni **admin** qiling
3. Quyidagi ruxsatlarni albatta yoqing:
   - ✅ **Delete messages** (xabarlarni o'chirish)
   - ✅ **Restrict members** (foydalanuvchilarni cheklash / mute qilish)

Shundan so'ng, guruhda kimdir link yoki fayl (APK ham) yuborsa:
- xabar avtomatik o'chiriladi
- yuboruvchi 5 daqiqaga guruhda yoza olmaydi

## 🎬 Video yuklab olish

Foydalanuvchi botga (shaxsiy chatda) Instagram yoki YouTube link yuborsa, bot uni avtomatik yuklab, video sifatida jo'natadi. Bu `yt-dlp` kutubxonasi orqali ishlaydi.

## 💬 Foydalanuvchi bilan muloqot

Foydalanuvchi botga xabar yozsa (link bo'lmasa), u avtomatik sizga (adminga) forward qilinadi. Javob berish uchun o'sha xabarga oddiy **Reply** qiling — javobingiz avtomatik foydalanuvchiga yetib boradi.

## 🚀 Railway'da hosting qilish

1. Loyihani GitHub'ga joylang (repo public yoki private bo'lishi mumkin — `.env` fayl `.gitignore` orqali chetlab o'tiladi)

2. [railway.app](https://railway.app) ga kiring → **New Project** → **Deploy from GitHub repo** → shu repo'ni tanlang

3. Agar loyiha GitHub'da papka ichida joylashgan bo'lsa (masalan `perfect_bot/bot.py`), Railway **Settings → Source → Root Directory** ga `perfect_bot` deb yozing

4. **Variables** bo'limiga o'ting va quyidagilarni qo'shing:
   - `BOT_TOKEN`
   - `ADMIN_ID`
   - `ADMIN_USERNAME`

5. Ma'lumotlarni saqlab qolish uchun **Volume** qo'shing (masalan `/data`) — Railway avtomatik `RAILWAY_VOLUME_MOUNT_PATH` beradi, `config.py` buni o'zi aniqlab oladi

6. **Deploy** tugmasini bosing

## 🛠 Muammolarni bartaraf etish

**ADMIN_ID to'g'ri ekanini tekshirish:**
Botga `/myid` deb yozing — u sizga aynan Telegram ID'ingizni ko'rsatadi. Shu raqamni Railway'dagi `ADMIN_ID` ga aynan shu ko'rinishda kiriting (bo'sh joy, tirnoqsiz).

**Guruhda mute ishlamayapti:**
Bot guruhda **admin** ekanligini va unga **"Restrict members"** huquqi berilganini tekshiring.

**Railway build xatosi "could not determine how to build the app":**
GitHub'da loyiha papka ichida bo'lsa, **Root Directory** ni `perfect_bot` qilib sozlang (yuqoriga qarang).

## 📁 Loyiha tuzilishi

```
perfect_bot/
├── bot.py              # Botni ishga tushiruvchi asosiy fayl
├── config.py           # Sozlamalar (token, admin ID, mute vaqti)
├── database.py         # SQLite ma'lumotlar bazasi funksiyalari
├── handlers/
│   ├── user.py         # Foydalanuvchi menyusi, video, forward
│   ├── admin.py        # Admin reply orqali javob berish
│   ├── group.py        # Guruh moderatsiyasi (link/fayl bloklash + mute)
│   └── downloader.py   # Video yuklab olish (yt-dlp)
├── downloads/            # Video yuklab olish uchun vaqtinchalik papka
├── requirements.txt
├── .env.example
└── README.md
```
