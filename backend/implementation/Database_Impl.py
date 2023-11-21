import sqlite3
from backend.entity.User import User
from backend.entity.Post import Post

# Pfad aus Sicht von app.py bedenken
DB_PATH = '../database/social_media.db'


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT, 
                  email TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  image TEXT, 
                  text TEXT, 
                  user_id INTEGER,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()


def add_user(user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email) VALUES (?, ?)", (user.username, user.email))
    user.id = c.lastrowid
    conn.commit()
    conn.close()
    return user


def add_post(post):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO posts (image, text, user_id) VALUES (?, ?, ?)", (post.image, post.text, post.user_id))
    conn.commit()
    conn.close()


def get_latest_post():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT posts.id, posts.image, posts.text, posts.timestamp, users.id, users.username, users.email 
                 FROM posts 
                 JOIN users ON posts.user_id = users.id 
                 ORDER BY posts.id DESC LIMIT 1''')
    row = c.fetchone()
    conn.close()
    if row:
        user = User(id=row[4], username=row[5], email=row[6])
        post = Post(id=row[0], image=row[1], text=row[2], user_id=row[3], timestamp=row[3])
        return post, user
    return None
