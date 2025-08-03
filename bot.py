import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()                             # загружаем переменные из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")        # читаем токен

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я RPG-бот. Готов к приключениям.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
