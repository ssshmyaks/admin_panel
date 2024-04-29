import sqlite3 as sq
import admin_keyboards
import config
import asyncio
import req
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

rt = Router()
bot = Bot(token=config.BOT_TOKEN)
db = sq.connect('database.db')
cur = db.cursor()

admin = req.get_admin()


@rt.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if str(user_id) in str(admin):
            await message.answer("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.admin_keyboard())
            await state.set_state(state=None)
        else:
            await message.answer('Нет прав ❌')
    else:
        pass


@rt.callback_query(F.data == 'back')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.admin_keyboard())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'admins')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.admins())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'support')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.support())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'users')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.users())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'check')
async def admin_check(call: CallbackQuery, state: FSMContext):
    with sq.connect('database.db'):
        cur.execute(f'SELECT id, tg FROM user')
        results = cur.fetchall()
        id_list = [row[0] for row in results]
        cur.execute(f'SELECT id, tg FROM banned')
        results = cur.fetchall()
        banned_list = [row[0] for row in results]
        await call.message.edit_text(f"В базе данных {id_list} ID пользователей 🧑\nЗаблокированных: {banned_list} 👮‍♂️", reply_markup=await admin_keyboards.admin_keyboard())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'add_admin')
async def admin_pass(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.admin_add.password)
        await call.message.edit_text("🚧 | Чтобы добавить администратора, введите пароль", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_add.password)
async def admin_id(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(req.admin_add.us)
    await message.delete()
    await message.answer("🚧 | Введите id администратора", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_add.us)
async def admin_addd(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(us=message.text)
    p = await state.get_data()
    if p['password'] == config.password:
        with sq.connect('database.db'):
            cur.execute("INSERT INTO admin (tg) VALUES (?)", (p['us'],))
            db.commit()
        await message.answer("✅ | Администратор добавлен", reply_markup=await admin_keyboards.admin_keyboard())
        await bot.send_message(p['us'], '😎 | Доступна команда /admin')
        await state.set_state(state=None)
    else:
        await message.answer("❌ | Неверный пароль", reply_markup=await admin_keyboards.admin_keyboard())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'del_admin')
async def admin_pass(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.admin_del.password)
        await call.message.edit_text("🚧 | Чтобы удалить администратора, введите пароль", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_del.password)
async def admin_id(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(req.admin_del.us)
    await message.delete()
    await message.answer("🚧 | Введите id администратора", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_del.us)
async def admin_dell(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    p = await state.get_data()
    if p['password'] == config.password:
        with sq.connect('database.db'):
            cur.execute("DELETE FROM admin WHERE tg = ?", (p['us'],))
            db.commit()
        await message.answer("✅ | Администратор удален", reply_markup=await admin_keyboards.admin_keyboard())
        await bot.send_message(p['us'], '❌ | Вам больше не доступна команда /admin')
        await state.set_state(state=None)
    else:
        await message.answer("❌ | Неверный пароль", reply_markup=await admin_keyboards.admin_keyboard())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'add_support')
async def support_id(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.support_add.us)
        await call.message.edit_text("🚧 | Введите id поддержки", reply_markup=await admin_keyboards.back())


@rt.message(req.support_add.us)
async def support_addd(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    p = await state.get_data()
    with sq.connect('database.db'):
        cur.execute("INSERT INTO support (tg) VALUES (?)", (p['us'],))
        db.commit()
    await message.answer("✅ | Поддержка добавлена", reply_markup=await admin_keyboards.admin_keyboard())
    await bot.send_message(p['us'], f'✅ | Доступен чат поддержки\n{config.support_chat_link}')
    try:
        await message.bot.unban_chat_member(chat_id=config.support_chat, user_id=p['us'])
    except:
        pass
    await state.set_state(state=None)


@rt.callback_query(F.data == 'del_support')
async def support_id(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.support_del.us)
        await call.message.edit_text("🚧 | Введите id поддержки", reply_markup=await admin_keyboards.back())


@rt.message(req.support_del.us)
async def support_dell(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    p = await state.get_data()
    with sq.connect('database.db'):
        cur.execute("DELETE FROM support WHERE tg = ?", (p['us'],))
        db.commit()
    await message.answer("✅ | Поддержка удалена", reply_markup=await admin_keyboards.admin_keyboard())
    await bot.send_message(p['us'], '❌ | Вам больше не доступен чат поддержки')
    await message.bot.ban_chat_member(chat_id=config.support_chat, user_id=p['us'])
    await state.set_state(state=None)


@rt.callback_query(F.data == 'distribute')
async def distribute(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.dist.dist_text)
        await call.message.edit_text('🧾 | Отправьте сообщение, которое желаете отправить всем пользователям этого бота', reply_markup=await admin_keyboards.back())


@rt.message(req.dist.dist_text)
async def distribute_send(message: Message, state: FSMContext):
    await state.update_data(dist_text=message.text)
    msg = await state.get_data()
    await state.set_state(state=None)
    with sq.connect('database.db'):
        cur.execute(f'SELECT id, tg FROM user')
        results = cur.fetchall()
        for row in results:
            print(f"id: {row[0]}, tg: {row[1]}")
            await bot.send_message(chat_id=row[1], text=msg['dist_text'])
            await asyncio.sleep(.05)
    await message.answer('✅ | Рассылка завершена', reply_markup=await admin_keyboards.back())


@rt.callback_query(F.data == 'ban')
async def ban_user(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.ban.us)
        await call.message.edit_text('🚧 | Отправьте id человека, которого хотите заблокировать', reply_markup=await admin_keyboards.back())


@rt.message(req.ban.us)
async def ban_user_s(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    user_id = await state.get_data()
    with sq.connect('database.db'):
        cur.execute("INSERT INTO banned (tg) VALUES (?)", (user_id['us'],))
        db.commit()
    await message.answer('✅ | Пользователь заблокирован', reply_markup=await admin_keyboards.admin_keyboard())


@rt.callback_query(F.data == 'unban')
async def unban_user(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.unban.us)
        await call.message.edit_text('🚧 | Отправьте id человека, которого хотите разблокировать', reply_markup=await admin_keyboards.back())


@rt.message(req.unban.us)
async def unban_user_s(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    user_id = await state.get_data()
    with sq.connect('database.db'):
        cur.execute("DELETE FROM banned WHERE tg = ?", (user_id['us'],))
        db.commit()
    await message.answer('✅ | Пользователь разблокирован', reply_markup=await admin_keyboards.admin_keyboard())
