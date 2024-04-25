import sqlite3 as sq
import config
import req
from create_db import create_table, add_referral
from aiogram import Router, Bot
from aiogram.methods import GetChat
from aiogram.filters import Command
from aiogram.types import Message

rt = Router()
bot = Bot(token=config.BOT_TOKEN)
db = sq.connect(r'database.db')
cur = db.cursor()

banned = req.get_banned()


@rt.message(Command("start"))
async def start(message: Message, b: Bot):
	user_id = message.from_user.id
	if str(user_id) in str(banned):
		await message.answer('Вы заблокированы в этом боте ❌')
	else:
		await message.answer('Привет!')
		try:
			creator_ref = message.text.split()[1]
			await create_table(int(creator_ref))
		except Exception as e:
			print(e)
		cur.execute("SELECT * FROM user WHERE tg = ?", (user_id,))
		user_exists = cur.fetchone() is not None
		if not user_exists:
			cur.execute("INSERT INTO user (tg) VALUES (?)", (user_id,))
			db.commit()
		refuser = await b(GetChat(chat_id=user_id))
		user_name = refuser.username
		with sq.connect('database.db'):
			table = 'a' + str(creator_ref)
			cur.execute(f"SELECT referral FROM {table}")
			result = cur.fetchall()
			for row in result:
				referral = row[0]

			if int(user_id) == int(creator_ref):
				await message.answer("❌ | Извините, но вы не можете быть своим рефералом!")
			if str(user_id) == str(referral):
				pass
			else:
				await b.send_message(creator_ref, f"🔥 | Пользователь @{user_name} присоединился к боту по вашей ссылке.")
				await add_referral(user_id, int(creator_ref))


@rt.message(Command("ref"))
async def ref_cmd(message: Message):
	user_id = message.from_user.id
	if str(user_id) in str(banned):
		await message.answer('Вы заблокированы в этом боте ❌')
	else:
		name_bot = 'AdmTest_shmxbot'
		URL_BOT = f'https://t.me/{name_bot}?start={user_id}'
		await message.answer(f"Ваша реферальная ссылка: {URL_BOT}")
