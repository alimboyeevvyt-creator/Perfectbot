"""
Link orqali (YouTube, Instagram, TikTok va h.k.) video yuklab olish.
yt-dlp kutubxonasidan foydalanadi.
"""
import os
import re
import uuid
import yt_dlp

from config import DOWNLOAD_DIR, MAX_FILE_SIZE_MB

URL_REGEX = re.compile(r"https?://[^\s]+")


def extract_url(text: str) -> str | None:
    """Xabar ichidan birinchi URL'ni topib qaytaradi."""
    match = URL_REGEX.search(text or "")
    return match.group(0) if match else None


def download_video(url: str) -> tuple[str | None, str | None]:
    """
    Berilgan link bo'yicha videoni yuklab oladi.
    Muvaffaqiyatli bo'lsa (fayl_yoli, None) qaytaradi.
    Xato bo'lsa (None, xato_matni) qaytaradi.
    """
    file_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "format": f"best[filesize<{MAX_FILE_SIZE_MB}M]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "max_filesize": MAX_FILE_SIZE_MB * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if os.path.exists(file_path):
                return file_path, None
            return None, "Video fayli topilmadi. Balki hajmi juda katta."
    except Exception as e:
        return None, f"Videoni yuklab bo'lmadi: {e}"


def cleanup_file(file_path: str):
    """Yuborilgandan keyin vaqtinchalik faylni o'chiradi."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass
