import sqlite3 as sq
from aiogram.fsm.state import State, StatesGroup
db = sq.connect('database.db')
cur = db.cursor()


class dist(StatesGroup):
    dist_text = State()


class admin_add(StatesGroup):
    password = State()
    us = State()


class support_add(StatesGroup):
    us = State()


class admin_del(StatesGroup):
    password = State()
    us = State()


class support_del(StatesGroup):
    us = State()


class ban(StatesGroup):
    us = State()


class unban(StatesGroup):
    us = State()


class quest(StatesGroup):
    text = State()


def get_banned():
    cur.execute("SELECT tg FROM banned")
    result = cur.fetchall()

    id_list = [row[0] for row in result]

    return id_list


def get_admin():
    cur.execute("SELECT tg FROM admin")
    result = cur.fetchall()

    id_list = [row[0] for row in result]

    return id_list


def extract_arg(arg):
    return arg.split()[1:]
