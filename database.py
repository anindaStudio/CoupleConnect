import sqlite3
import os

# 📍 Database path (same folder)
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

# ---------------- CREATE TABLE ----------------
def create_table():
    conn = connect_db()
    c = conn.cursor()

    # 👤 Users Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        partner TEXT
    )
    """)

    # 💌 Messages Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        sender TEXT,
        receiver TEXT,
        message TEXT
    )
    """)

    # 🎮 Quiz Table (Added UNIQUE constraint to prevent duplicates)
    c.execute("""
    CREATE TABLE IF NOT EXISTS quiz(
        user TEXT,
        question TEXT,
        answer TEXT,
        UNIQUE(user, question)
    )
    """)

    conn.commit()
    conn.close()

# ---------------- USER FUNCTIONS ----------------
def add_user(u, p):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, partner) VALUES (?, ?, ?)", (u, p, None))
    conn.commit()
    conn.close()

def login(u, p):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    data = c.fetchone()
    conn.close()
    return data

def get_user(u):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (u,))
    data = c.fetchone()
    conn.close()
    return data

def set_partner(u, p):
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE users SET partner=? WHERE username=?", (p, u))
    conn.commit()
    conn.close()

# ---------------- MESSAGE FUNCTIONS ----------------
def send_message(sender, receiver, msg):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)", (sender, receiver, msg))
    conn.commit()
    conn.close()

def get_messages(user):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT sender, message FROM messages WHERE receiver=?", (user,))
    data = c.fetchall()
    conn.close()
    return data

# ---------------- QUIZ FUNCTIONS (Improved) ----------------
def save_answer(user, question, answer):
    conn = connect_db()
    c = conn.cursor()
    # "INSERT OR REPLACE" use koray jodi same question thake, tobe answer update hobe
    c.execute("INSERT OR REPLACE INTO quiz (user, question, answer) VALUES (?, ?, ?)", (user, question, answer))
    conn.commit()
    conn.close()

def get_partner_answer(partner, question):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT answer FROM quiz WHERE user=? AND question=?", (partner, question))
    data = c.fetchone()
    conn.close()
    return data

def get_all_answers(user):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT question, answer FROM quiz WHERE user=?", (user,))
    data = c.fetchall()
    conn.close()
    return data

# ---------------- LOVE SCORE FUNCTIONS ----------------
def count_messages(user):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages WHERE sender=?", (user,))
    result = c.fetchone()
    data = result[0] if result else 0
    conn.close()
    return data

def count_matches(user, partner):
    conn = connect_db()
    c = conn.cursor()

    # Finding common questions answered by both
    c.execute("""
    SELECT q1.answer, q2.answer 
    FROM quiz q1 JOIN quiz q2 
    ON q1.question = q2.question
    WHERE q1.user=? AND q2.user=?
    """, (user, partner))

    data = c.fetchall()
    conn.close()

    match = 0
    for a, b in data:
        if a.strip().lower() == b.strip().lower(): # added strip() to handle extra spaces
            match += 1

    return match, len(data)