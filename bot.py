import os
import json
import sqlite3
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot       = Bot(token=BOT_TOKEN)
dp        = Dispatcher(bot)
DB        = "heroes.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nick TEXT,
            gender TEXT,
            race TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_hero(data: dict):
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO heroes (nick, gender, race) VALUES (?, ?, ?)",
        (data.get('nick'), data.get('gender'), data.get('race'))
    )
    conn.commit()
    conn.close()
    print("💾 Hero saved to DB:", data)

# Отладочный хендлер, который ловит ВСЁ
@dp.message_handler(content_types=types.ContentType.ANY)
async def debug_all(message: types.Message):
    print("\n=== GOT MESSAGE ===")
    print("type:", message.content_type)
    print("text:", message.text)
    print("web_app_data:", getattr(message, "web_app_data", None))
    print("full object:", message)
    # не отвечаем тут — просто лог

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Отправь /create, чтобы создать героя.")

@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message):
    print("🔹 /create received")
    webapp_url = "https://valentingorovik.github.io/tg_bot/index.html"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text="🚀 Создать героя",
        web_app=types.WebAppInfo(url=webapp_url)
    ))
    await message.answer("Нажми кнопку, чтобы открыть форму:", reply_markup=kb)

# Специально на строку 'web_app_data'
@dp.message_handler(content_types=['web_app_data'])
async def webapp_handler(message: types.Message):
    print("🔥 web_app_data handler called!")
    raw = message.web_app_data.data
    print("📨 raw data string:", raw)
    try:
        data = json.loads(raw)
    except Exception as e:
        print("❌ JSON parse error:", e)
        return await message.answer("❗ Неверный формат данных.")
    print("✅ Parsed payload:", data)

    # Сохраняем и отвечаем
    save_hero(data)
    await message.answer(f"✅ Герой сохранён: {data}")

if __name__ == '__main__':
    print("🗄  Инициализируем базу…")
    init_db()
    print("🚀 Запускаю бота…")
    # НЕ пропускаем никакие новые обновления
    executor.start_polling(dp, skip_updates=False)
