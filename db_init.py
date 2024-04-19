import sqlite3

conn = sqlite3.connect('baby-v.db')
cursor = conn.cursor()

"""
cursor.execute('''
    DROP TABLE users
''')

cursor.execute('''
    DROP TABLE babies
''')

cursor.execute('''
    DROP TABLE sleep_entries
''')

cursor.execute('''
    DROP TABLE food_entries
''')
"""

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT
)
''')

cursor.execute('''
       CREATE TABLE IF NOT EXISTS babies (
           id INTEGER PRIMARY KEY,
           user_id INTEGER,
           baby_name TEXT,
           date_of_birth DATE,
           hour_of_birth TIME,
           birth_weight REAL,
           birth_height REAL,
           FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS sleep_entries (
            id INTEGER PRIMARY KEY,
            baby_id INTEGER,
            start_hour TEXT NOT NULL,
            end_hour TEXT NOT NULL,
            sleep_date DATE,
            notes TEXT,
            FOREIGN KEY(baby_id) REFERENCES babies(id)
)
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_entries (
            id INTEGER PRIMARY KEY,
            baby_id INTEGER,
            feed_hour TEXT NOT NULL,
            feed_date DATE,
            ml INTEGER,
            notes TEXT,
            FOREIGN KEY(baby_id) REFERENCES babies(id)
)
''')


conn.commit()
conn.close()
