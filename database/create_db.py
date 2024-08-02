import sqlite3 as sq

db = sq.connect(r'/home/ssshmyaks/PycharmProjects/admin_panel/database/database.db')
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

# cur.execute("INSERT INTO admin (tg) VALUES (?)", (config.admin,))
# db.commit()


async def create_table(creator_ref: int):
    table = 'a' + str(creator_ref)
    with sq.connect('database.db'):
        cur.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY,
                    referral INTEGER
                    )''')
        db.commit()


async def add_referral(user_id: int, creator_ref: int):
    table = 'a' + str(creator_ref)
    with sq.connect('database.db'):
        cur.execute(f"SELECT * FROM {table} WHERE referral = ?", (user_id,))
        user_exists = cur.fetchone() is not None
        if not user_exists:
            cur.execute(f"INSERT INTO {table} (referral) VALUES (?)", (user_id,))
            db.commit()
