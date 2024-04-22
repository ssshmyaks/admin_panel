from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

rt = Router()


async def admin_keyboard():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Проверка пользователей",
                        callback_data="check"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Рассылка",
                        callback_data="distribute"
                    )
                ]
            ]
        )


async def clear_id():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Очистить",
                        callback_data="clear"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Назад ↩",
                        callback_data="back"
                    )
                ]
            ]
        )
