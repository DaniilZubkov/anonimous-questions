import sqlite3
import time


db = sqlite3.connect('database.db')


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # def create_users_table(self):
    #     with self.connection:
    #         self.cursor.execute("""
    #             CREATE TABLE IF NOT EXISTS users (
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 user_id INTEGER NOT NULL,
    #                 nickname TEXT,
    #                 timesub DATETIME,
    #                 signup DATETIME
    #             )
    #         """)

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE users SET nickname=? WHERE user_id=?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup=? WHERE user_id=?", (signup, user_id,))


    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT nickname FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname



    def set_sender(self, user_id, sender):
        with self.connection:
            return self.cursor.execute("UPDATE users SET sender=? WHERE user_id=?", (sender, user_id,))

    def get_sender(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT sender FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                sender = str(row[0])
            return sender



    def set_sender2(self, user_id, sender2):
        with self.connection:
            return self.cursor.execute("UPDATE users SET sender2=? WHERE user_id=?", (sender2, user_id,))

    def get_sender2(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT sender2 FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                sender = str(row[0])
            return sender
