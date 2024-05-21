# Телега 
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os
from agrigation import Agrigation
import tests
import unittest

unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromModule(tests))

bot = Bot(token=os.environ.get('TELEGRAM_ACCESS_TOKEN'))
dp = Dispatcher()

print('Telegram-bot: launched!')

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hi, {message.from_user.full_name}!")

@dp.message()
async def get_dataset(message: types.Message):
    try:
        request = eval(message.text)
        if list(request.keys()) == ['dt_from', 'dt_upto', 'group_type']:
            if list(request.values()) != ['', '', '']:
                await message.answer(Agrigation(request).dataset())
            
            else:
                raise Exception('not valid values')

        else:
            raise Exception('not valid keys')
    except Exception:
        await message.answer('Невалидный запос. Пример запроса: {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))