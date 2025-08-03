import os
import json
import sqlite3
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(bot)

DB_PATH = "heroes.db"

def init_db():
    """Создаёт файл heroes.db и таблицу heroes, если они ещё не существуют."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nick TEXT NOT NULL,
            gender TEXT NOT NULL,
            race  TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("👋 Привет! Отправь /create, чтобы начать создание героя.")

@dp.message_handler(commands=['create'])
async def create_handler(message: types.Message):
    webapp_url = "https://valentingorovik.github.io/tg_bot/index.html"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text="🚀 Создать героя",
        web_app=types.WebAppInfo(url=webapp_url)
    ))
    await message.answer("Нажми кнопку, чтобы открыть форму создания героя:", reply_markup=kb)

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def webapp_handler(message: types.Message):
    raw = message.web_app_data.data
    try:
        data = json.loads(raw)  # {'nick':..., 'gender':..., 'race':...}
    except json.JSONDecodeError:
        return await message.answer("❗ Не удалось разобрать данные.")

    # Сохраняем в SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO heroes (nick, gender, race) VALUES (?, ?, ?)",
        (data['nick'], data['gender'], data['race'])
    )
    conn.commit()
    conn.close()

    # Подтверждаем пользователю
    await message.answer(
        f"✅ Ваш герой сохранён:\n"
        f"Ник:   {data['nick']}\n"
        f"Пол:   {data['gender']}\n"
        f"Раса:  {data['race']}"
    )

if __name__ == '__main__':
    # 1) Синхронно инициализируем базу
    print("Инициализируем базу…")
    init_db()

    # 2) Запускаем бота
    print("Запускаем бота…")
    executor.start_polling(dp, skip_updates=True)
