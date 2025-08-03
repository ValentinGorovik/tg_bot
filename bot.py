import os, json, sqlite3, asyncio, logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# — Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# — Токен и БД
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB        = "heroes.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY,
        nick TEXT NOT NULL,
        gender TEXT NOT NULL,
        race TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)
    con.commit()
    con.close()
    logger.info("✅ DB ready")

# — /start принимает аргумент deep-link
async def cmd_start(message: Message):
    args = message.get_args()
    if args:
        try:
            data = json.loads(args)
            logger.info("💾 Received via deep-link: %s", data)
            con = sqlite3.connect(DB)
            con.execute(
                "INSERT INTO heroes (nick, gender, race) VALUES (?, ?, ?)",
                (data["nick"], data["gender"], data["race"])
            )
            con.commit()
            con.close()
            await message.answer(
              f"✅ Сохранено:\n"
              f"Ник: {data['nick']}\n"
              f"Пол: {data['gender']}\n"
              f"Раса: {data['race']}"
            )
            return
        except Exception as e:
            logger.error("Deep-link error: %s", e)
    await message.answer("👋 Привет! Напишите /create")

# — /create шлёт кнопку
async def cmd_create(message: Message):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
    kb = InlineKeyboardMarkup(inline_keyboard=[[
      InlineKeyboardButton(
        text="🚀 Создать героя",
        web_app=WebAppInfo(url="https://valentingorovik.github.io/tg_bot/index.html")
      )
    ]])
    await message.answer("Нажмите кнопку ниже:", reply_markup=kb)

async def main():
    init_db()
    bot = Bot(BOT_TOKEN)
    dp  = Dispatcher()
    dp.message.register(cmd_start,  Command("start"))
    dp.message.register(cmd_create, Command("create"))
    logger.info("🚀 Polling…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
