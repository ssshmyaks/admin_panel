from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

rt = Router()


async def admin_keyboard():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Проверка пользователей 📊",
                        callback_data="check"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Рассылка ✏",
                        callback_data="distribute"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Администраторы 🔥",
                        callback_data="admins"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Поддержка 🧰",
                        callback_data="support"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Пользователи 🧑",
                        callback_data="users"
                    )
                ]
            ]
        )


async def admins():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить администратора ✅",
                    callback_data="add_admin"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Удалить администратора ❎",
                    callback_data="del_admin"
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


async def support():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить поддержку ✅",
                    callback_data="add_support"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Удалить поддержку ❎",
                    callback_data="del_support"
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


async def users():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Заблокировать пользователя ⚔",
                    callback_data="ban"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Разблокировать пользователя 🛡",
                    callback_data="unban"
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


async def back():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад ↩",
                    callback_data="back"
                )
            ]
        ]
    )
