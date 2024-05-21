# Телега 
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os

bot = Bot(token=os.environ.get('TELEGRAM_ACCESS_TOKEN'))

dp = Dispatcher()
print('Telegram-bot запущен!')

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Прив")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))