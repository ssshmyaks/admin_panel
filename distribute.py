import asyncio
import config
import sqlite3 as sq
from aiogram import Router, F, Bot
from aiogram.types import callback_query, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

rt = Router()
bot = Bot(token=config.BOT_TOKEN)
cur = db.cursor()
db = sq.connect(r'C:\Users\super\Projects\adminpanel\database.db')


class tg(StatesGroup):
	dist_text = State()


@rt.callback_query(F.data == 'distribute')
async def distribute(call: callback_query, state: FSMContext):
	await state.set_state(tg.dist_text)
	await call.message.answer('Отправьте сообщение, которое желаете отправить всем пользователям этого бота')


@rt.message(tg.dist_text)
async def distribute_send(message: Message, state: FSMContext):
	await state.update_data(dist_text=message.text)
	msg = await state.get_data()
	with sq.connect('database.db'):
		cur.execute(f'SELECT id, tg, date FROM accounts')
		results = cur.fetchall()
		for row in results:
			print(f"id: {row[0]}, tg: {row[1]}, date: {row[2]}")
			await bot.send_message(chat_id=row[1], text=msg['dist_text'])
			await asyncio.sleep(.05)
	await message.answer('Рассылка завершена')
