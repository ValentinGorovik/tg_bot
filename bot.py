import os, json, sqlite3
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(bot)
DB   = "heroes.db"

def init_db():
    conn = sqlite3.connect(DB)
    c    = conn.cursor()
    c.execute("""
      CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nick TEXT, gender TEXT, race TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)
    conn.commit()
    conn.close()

@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    await msg.answer("👋 Привет! Напиши /create")

@dp.message_handler(commands=['create'])
async def cmd_create(msg: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
      "🚀 Создать героя",
      web_app=types.WebAppInfo(
        url="https://valentingorovik.github.io/tg_bot/index.html"
      )
    ))
    await msg.answer("Нажми кнопку:", reply_markup=kb)

@dp.message_handler(content_types=['web_app_data'])
async def webapp_handler(msg: types.Message):
    raw = msg.web_app_data.data
    data = json.loads(raw)
    # сохраняем
    conn = sqlite3.connect(DB)
    c    = conn.cursor()
    c.execute(
      "INSERT INTO heroes (nick, gender, race) VALUES (?, ?, ?)",
      (data['nick'], data['gender'], data['race'])
    )
    conn.commit()
    conn.close()
    await msg.answer(f"✅ Сохранено: {data}")

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
