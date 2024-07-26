import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import keyboards
import lexicon
import logics
import config
import states


TOKEN = "6368678074:AAEyPz9q_PLp7DGws1Ltk2AIHwDEEneEL1Q"
storage = MemoryStorage()
dp = Dispatcher(storage=storage)



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=await keyboards.general_markup_function())

@dp.message(Command("menu"))
async def command_admin_handler(message: Message) -> None:
    if await logics.create_prices_function(message.chat.id):
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
    prices = await logics.show_prices_function('files/prices.json')
    msg = f"CNY/RUB -> {prices['china']}\n\nUSD/RUB -> {prices['usa']}"
    await message.answer(text=msg)

@dp.message(F.text.startswith("Запросить"))
async def call_help_function(message: Message):
    await bot.send_message(chat_id=config.DEV_ID, text=f"Запрос на обратную связь -> @{message.from_user.username}")

@dp.callback_query(F.data.in_({'xslx', 'doc'}))
async def show_blank_function(callback: CallbackQuery):
    if callback.data == 'doc':
        await callback.message.answer(text=lexicon.DOC_BLANK_MEAASGE)
    else:
        await bot.send_document(chat_id=callback.message.chat.id, document=FSInputFile('files/Сорбент-02.07.2024.xlsx'))

@dp.callback_query(F.data == 'all')
async def show_all_function(callback: CallbackQuery):
    await callback.message.answer(text="Возможности Бота", reply_markup=await keyboards.general_markup_function())

@dp.callback_query(F.data == 'prices')
async def replace_prices_function(callback: CallbackQuery):
    await callback.message.answer(text="Изменить курсы валют", reply_markup=await keyboards.replace_prices_markup_function())

@dp.callback_query(F.data.in_({'replace_china', 'replace_usa'}))
async def choose_replace_prices_function(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'replace_china':
        await state.set_state(states.Prices.china)
    else:
        await state.set_state(states.Prices.usa)
    await callback.message.answer("Введите обновленный курс")

@dp.message(states.Prices.china)
async def new_price_china_function(message: Message, state: FSMContext):
    await state.update_data(china=message.text)
    result_china = await state.get_data()
    await logics.add_prices_function('files/prices.json', china=result_china['china'])
    await message.answer(text=f"Курс CNY/RUB обновлен")

@dp.message(states.Prices.usa)
async def new_price_usa_function(message: Message, state: FSMContext):
    await state.update_data(usa=message.text)
    result_usa = await state.get_data()
    await logics.add_prices_function('files/prices.json', usa=result_usa['usa'])
    await message.answer(text=f"Курс USD/RUB обновлен")




async def main() -> None:
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())