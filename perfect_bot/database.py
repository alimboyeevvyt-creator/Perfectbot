"""
SQLite ma'lumotlar bazasi bilan ishlash.

Jadvallar:
- users: botdan foydalangan barcha foydalanuvchilar (broadcast uchun)
- apk_files: admin yuklagan APK fayllar ro'yxati
- messages_map: admin javobini to'g'ri foydalanuvchiga yetkazish uchun
  (admin guruhidagi forward qilingan xabar ID -> foydalanuvchi ID)
"""
import sqlite3
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS apk_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            telegram_file_id TEXT,
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Admin panelida forward qilingan xabarni kim yozganini bilish uchun
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages_map (
            admin_message_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id: int, username: str, first_name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
        (user_id, username, first_name),
    )
    conn.commit()
    conn.close()


def get_all_user_ids():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    rows = cur.fetchall()
    conn.close()
    return [row["user_id"] for row in rows]


def get_user_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM users")
    row = cur.fetchone()
    conn.close()
    return row["cnt"]


def save_message_map(admin_message_id: int, user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO messages_map (admin_message_id, user_id) VALUES (?, ?)",
        (admin_message_id, user_id),
    )
    conn.commit()
    conn.close()


def get_user_from_message(admin_message_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id FROM messages_map WHERE admin_message_id = ?",
        (admin_message_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row["user_id"] if row else None


def add_apk(name: str, file_path: str, telegram_file_id: str = None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO apk_files (name, file_path, telegram_file_id) VALUES (?, ?, ?)",
        (name, file_path, telegram_file_id),
    )
    conn.commit()
    conn.close()


def get_all_apks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apk_files ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_apk_by_id(apk_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apk_files WHERE id = ?", (apk_id,))
    row = cur.fetchone()
    conn.close()
    return row


def delete_apk(apk_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM apk_files WHERE id = ?", (apk_id,))
    conn.commit()
    conn.close()
