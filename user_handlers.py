from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import sqlite3 as sq
from datetime import datetime

db = sq.connect(r'C:\Users\super\Projects\adminpanel\database.db')
cur = db.cursor()
rt = Router()


@rt.message(Command("start"))
async def start(message: Message):
	user_id = message.from_user.id
	with sq.connect('database.db'):
		cur.execute("SELECT * FROM accounts WHERE tg = ?", (user_id,))
		user_exists = cur.fetchone() is not None
		if not user_exists:
			cur.execute("INSERT INTO accounts (tg, date) VALUES (?, ?)", (user_id, datetime.now()))
			db.commit()
			await message.answer('Вы добавлены в базу данных')
		else:
			await message.answer('Вы уже есть в базе данных')
