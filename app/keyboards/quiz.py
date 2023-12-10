from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_keyboard_choose_type_of_quiz(list_of_data: list[str]):
    builder = InlineKeyboardBuilder()
    for data in list_of_data:
        builder.add(types.InlineKeyboardButton(
            text=data,
            callback_data=data
        ))
    return builder.as_markup()


def get_help_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


