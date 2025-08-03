import os, json, sqlite3
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor

load_dotenv()
BOT_TOKEN    = os.getenv("BOT_TOKEN")
BOT_USERNAME = "bestwarrior_bot"  # без "@"

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(bot)

DB_PATH = "heroes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nick TEXT NOT NULL,
            gender TEXT NOT NULL,
            race TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    arg = message.get_args()
    if arg:
        try:
            data = json.loads(arg)
            # сохраняем payload из deep-link
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute(
                "INSERT INTO heroes (nick, gender, race) VALUES (?, ?, ?)",
                (data['nick'], data['gender'], data['race'])
            )
            conn.commit()
            conn.close()
            return await message.answer(
                f"✅ [deep-link] Герой сохранён:\n"
                f"Ник: {data['nick']}\nПол: {data['gender']}\nРаса: {data['race']}"
            )
        except Exception as e:
            print("❌ deep-link error:", e)
    await message.answer("👋 Привет! Отправь /create для начала.")

@dp.message_handler(commands=['create'])
async def create_handler(message: types.Message):
    webapp_url = "https://valentingorovik.github.io/tg_bot/index.html"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "🚀 Создать героя", web_app=types.WebAppInfo(url=webapp_url)
    ))
    await message.answer("Нажми кнопку:", reply_markup=kb)

@dp.message_handler(content_types=['web_app_data'])
async def webapp_handler(message: types.Message):
    raw = message.web_app_data.data
    data = json.loads(raw)
    # сохраняем payload из WebApp
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO heroes (nick, gender, race) VALUES (?, ?, ?)",
        (data['nick'], data['gender'], data['race'])
    )
    conn.commit()
    conn.close()
    await message.answer(
        f"✅ [WebApp] Герой сохранён:\n"
        f"Ник: {data['nick']}\nПол: {data['gender']}\nРаса: {data['race']}"
    )

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
