import sqlite3 as sq
import config
from create_db import create_table
from aiogram import Router, Bot
from aiogram.methods import GetChat
from aiogram.filters import Command
from aiogram.types import Message


rt = Router()
bot = Bot(token=config.BOT_TOKEN)
db = sq.connect(r'database.db')
cur = db.cursor()


def get_banned():
	cur.execute("SELECT tg FROM banned")
	result = cur.fetchall()

	id_list = [row[0] for row in result]

	return id_list


banned = get_banned()


@rt.message(Command("start"))
async def start(message: Message, bot: Bot):
	user_id = message.from_user.id
	if str(user_id) in str(banned):
		await message.answer('Вы заблокированы в этом боте')
	else:
		await message.answer('Привет!')
		try:
			creator_ref = message.text.split()[1]
		except Exception as e:
			print(e)
		user = await bot(GetChat(chat_id=user_id))
		username = user.username
		with sq.connect('database.db'):
			cur.execute("SELECT * FROM user WHERE tg = ?", (user_id,))
			user_exists = cur.fetchone() is not None
			if not user_exists:
				cur.execute("INSERT INTO user (tg) VALUES (?)", (user_id,))
				db.commit()
		try:
			if int(user_id) == int(creator_ref):
				await message.answer("Извините, но вы не можете быть своим рефералом!")
			else:
				await bot.send_message(creator_ref, f"Пользователь @{username} присоединился к боту по вашей ссылке.")
				await create_table(user_id, username)
		except Exception as e:
			print(e)


@rt.message(Command("ref"))
async def ref_cmd(message: Message):
	user_id = message.from_user.id
	if str(user_id) in str(banned):
		await message.answer('Вы заблокированы в этом боте')
	else:
		name_bot = 'AdmTest_shmxbot'
		URL_BOT = f'https://t.me/{name_bot}?start={user_id}'
		await message.answer(f"Ваша реферальная ссылка: {URL_BOT}")
