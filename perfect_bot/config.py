"""
PERFECT bot uchun konfiguratsiya fayli.

Muhim: BOT_TOKEN ni albatta o'zingiznikiga almashtiring!
"""
import os
from dotenv import load_dotenv

load_dotenv()

# BotFather'dan olingan bot tokeni
# .env faylida BOT_TOKEN=123456:ABC-DEF... shaklida yozing
BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN_BU_YERGA")

# Sizning shaxsiy Telegram ID'ingiz (foydalanuvchi xabarlari shu ID'ga forward qilinadi)
# ID ni bilish uchun botga /myid deb yozing
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Bot yasatish uchun murojaat qilinadigan Telegram username (@ belgisisiz)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Alimboyeevv")

# Railway'da "Volume" ulangan bo'lsa, undagi doimiy papkadan foydalaniladi
DATA_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", os.path.dirname(__file__))

# Ma'lumotlar bazasi fayli
DB_PATH = os.path.join(DATA_DIR, "perfect_bot.db")

# Video yuklab olish uchun vaqtinchalik papka
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Guruhda taqiqlangan narsalar (True = o'chirilsin)
BLOCK_LINKS = True
BLOCK_FILES = True

# Qoida buzilganda necha daqiqaga "mute" qilinsin (yoza olmaydi)
MUTE_MINUTES = 5

# Telegram fayl yuklash limiti (bot API orqali ~50MB gacha yuborish mumkin)
MAX_FILE_SIZE_MB = 50
