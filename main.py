import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import keyboards
import lexicon
import logics
import config


TOKEN = "6368678074:AAEyPz9q_PLp7DGws1Ltk2AIHwDEEneEL1Q"
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=await keyboards.general_markup_function())

@dp.message(Command("menu"))
async def command_admin_handler(message: Message) -> None:
    if logics.create_prices_function(message, message.chat.id):
        await message.answer(text="Выберите команду", reply_markup=await keyboards.admin_markup_function())
    else:
        await message.answer(text=lexicon.USER_LOCK_MESSAGE)

@dp.message(F.text == "Информация о Trade With China")
async def info_bot_function(message: Message):
    await message.answer(text=lexicon.INFO_BOT_MESSAGE)

@dp.message(F.text == "Условия работы с Trade With China")
async def conditions_bot_function(message: Message):
    await message.answer(text=lexicon.CONDITIONS_BOT_MESSAGE)

@dp.message(F.text == "Бланк заказа в Trade With China")
async def blank_bot_function(message: Message):
    await message.answer(text=lexicon.BLANK_BOT_MESSAGE, reply_markup=await keyboards.blank_markup_function())

@dp.message(F.text == "Группа Trade With China VK")
async def group_bot_function(message: Message):
    await message.answer(text=lexicon.GROUP_BOT_MESSAGE, reply_markup=await keyboards.group_markup_function())

@dp.message(F.text == "Узнать актуальный курс")
async def actual_price_function(message: Message):
    await message.answer(text="")

@dp.message(F.text.startswith("Запросить"))
async def call_help_function(message: Message):
    await bot.send_message(chat_id=config.DEV_ID, text=f"Запрос на обратную связь -> @{message.from_user.username}")



async def main() -> None:
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())