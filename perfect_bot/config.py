"""
PERFECT bot uchun konfiguratsiya fayli.

Muhim: BOT_TOKEN va ADMIN_ID ni albatta o'zingiznikiga almashtiring!
"""
import os
from dotenv import load_dotenv

load_dotenv()

# BotFather'dan olingan bot tokeni
# .env faylida BOT_TOKEN=123456:ABC-DEF... shaklida yozing
BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN_BU_YERGA")

# Sizning shaxsiy Telegram ID'ingiz (admin panelga faqat shu ID kira oladi)
# ID ni bilish uchun @userinfobot ga /start yozing
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Ma'lumotlar bazasi fayli
DB_PATH = os.path.join(os.path.dirname(__file__), "perfect_bot.db")

# APK fayllar saqlanadigan papka
APK_DIR = os.path.join(os.path.dirname(__file__), "apk_files")
os.makedirs(APK_DIR, exist_ok=True)

# Video yuklab olish uchun vaqtinchalik papka
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Guruhda taqiqlangan narsalar (True = o'chirilsin)
BLOCK_LINKS = True
BLOCK_FILES = True

# Telegram fayl yuklash limiti (bot API orqali ~50MB gacha yuborish mumkin)
MAX_FILE_SIZE_MB = 50
