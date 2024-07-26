from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton
import asyncio

import lexicon


async def general_markup_function():
    builder = ReplyKeyboardBuilder()
    for index, data in enumerate(lexicon.GENERAL_MARKUP_NAMES):
        if index in [0, 1, 2, 5]:
            builder.button(text=f"{data} {lexicon.HEADERNAME}")
        elif index == 3:
            builder.button(text=f"{data} {lexicon.HEADERNAME} VK")
        else:
            builder.button(text=data)
    builder.adjust(1)
    return builder.as_markup()


async def blank_markup_function():
    builder = InlineKeyboardBuilder()
    builder.button(text="XSLX форма", callback_data='xslx')
    builder.button(text='Текстовая форма', callback_data='doc')
    builder.adjust(1)
    return builder.as_markup()


async def group_markup_function():
    builder = InlineKeyboardBuilder()
    builder.button(text="VK", url="https://vk.com/tradewithchinaru")
    builder.adjust(1)
    return builder.as_markup()


async def prices_markup_funcion():
    builder = InlineKeyboardBuilder()
    builder.button(text="CNY/RUB", callback_data="china")
    builder.button(text="USD/RUB", callback_data="usa")
    builder.adjust(1)
    return builder.as_markup()


async def admin_markup_function():
    builder = InlineKeyboardBuilder()
    builder.button(text="Просмотр функционала", callback_data="all")
    builder.button(text="Изменить курсы валют", callback_data="prices")
    builder.adjust(1)
    return builder.as_markup()


async def replace_prices_markup_function():
    builder = InlineKeyboardBuilder()
    builder.button(text="CNY/RUB", callback_data='replace_china')
    builder.button(text="USD/RUB", callback_data='replace_usa')
    builder.adjust(1)
    return builder.as_markup()

