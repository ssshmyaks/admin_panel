import sqlite3 as sq
import config
import req
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

rt = Router()
db = sq.connect('database.db')
cur = db.cursor()


@rt.message(Command("support"))
async def client_question(message: Message, state: FSMContext, bot: Bot):
	try:
		await state.set_state(req.quest.text)
		await message.answer("🎟 | Введите ваш вопрос")

	except Exception as e:
		cid = message.chat.id
		await message.answer("⚠ | Произошла ошибка")
		await bot.send_message(config.admin, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`", parse_mode='Markdown')


@rt.message(req.quest.text)
async def question(message: Message, state: FSMContext, bot: Bot):
	await state.update_data(quest=message.text)
	if message.from_user.username is None:
		who = "Ник не установлен"
	else:
		who = "@" + message.chat.username
	request = await state.get_data()
	await message.reply("🕒 | Ожидайте ответа от тех.поддержки.")
	await bot.send_message(config.support_chat, f'✉ | Новый вопрос\nОт: {who}\nВопрос: {request['quest']}')
	await bot.send_message(config.support_chat, f'📝 Чтобы ответить на вопрос введите `/answer {message.chat.id}`', parse_mode='Markdown')


@rt.message(Command("answer"))
async def answer(message: Message, bot: Bot):
	args = req.extract_arg(message.text)
	if len(args) >= 2:
		chatid = str(args[0])
		args.pop(0)
		answr = ""
		for ot in args:
			answr += ot + " "
	else:
		await message.reply('⚠ | Укажите аргументы команды')
		return
	await bot.send_message(chatid, f'*Ответ от поддержки:*\n{answr}', parse_mode='HTML')
	await message.answer('Отправлено ✅')
