import sqlite3 as sq
import admin_keyboards
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

admin_id = '825627855'
rt = Router()
db = sq.connect(r'C:\Users\super\Projects\adminpanel\database.db')
cur = db.cursor()


@rt.message(Command("admin"))
async def admin(message: Message):
    if not str(message.from_user.id) in admin_id:
        await message.answer('Нет прав')
        return
    await message.answer("Вы вошли в админ панель ✅", reply_markup=await admin_keyboards.admin_keyboard())


@rt.callback_query(F.data == 'back')
async def admin(call: CallbackQuery):
    await call.message.edit_text("Вы вошли в админ панель ✅", reply_markup=await admin_keyboards.admin_keyboard())


@rt.callback_query(F.data == 'check')
async def admin_check(call: CallbackQuery):
    with sq.connect('database.db'):
        cur.execute(f'SELECT id, tg, date FROM accounts')
        results = cur.fetchall()
        for row in results:
            print(f"id: {row[0]}, tg: {row[1]}, date: {row[2]}")
        await call.message.edit_text(f"В базе данных {row[0]} ID пользователей.", reply_markup=await admin_keyboards.clear_id())


@rt.callback_query(F.data == 'clear')
async def admin_clear(call: CallbackQuery):

    await call.message.edit_text("Список ID пользователей очищен.", reply_markup=await admin_keyboards.admin_keyboard())
