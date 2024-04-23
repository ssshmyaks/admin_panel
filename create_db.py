import config
import sqlite3 as sq

db = sq.connect(r'C:\Users\super\Projects\adminpanel\database.db')
cur = db.cursor()


cur.execute('''  
    CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    tg INTEGER
    )''')

cur.execute('''  
    CREATE TABLE IF NOT EXISTS banned(
    id INTEGER PRIMARY KEY,
    tg INTEGER
    )''')

cur.execute('''  
    CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY,
    tg INTEGER
    )''')

cur.execute('''  
    CREATE TABLE IF NOT EXISTS support(
    id INTEGER PRIMARY KEY,
    tg INTEGER
    )''')


with sq.connect('database.db'):
    cur.execute("INSERT INTO admin (tg) VALUES (?)", (config.admin,))
    db.commit()


def create_table(user_id: int, referral: str):
    table = 'a' + str(user_id)

    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {table} (
    id INTEGER PRIMARY KEY,
    referral TEXT NOT NULL,
    act INTEGER
    )''')

    cur.execute(f'INSERT INTO {table} (referral, act) VALUES (?, ?)', (referral, 0))
    db.commit()
