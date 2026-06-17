import sqlite3

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        role TEXT
    )''')

    # Batch
    cur.execute('''CREATE TABLE IF NOT EXISTS batch(
        id INTEGER PRIMARY KEY,
        name TEXT,
        start TEXT,
        end TEXT
    )''')

    # Technology
    cur.execute('''CREATE TABLE IF NOT EXISTS technology(
        id INTEGER PRIMARY KEY,
        name TEXT
    )''')

    # Rounds config
    cur.execute('''CREATE TABLE IF NOT EXISTS rounds(
        id INTEGER PRIMARY KEY,
        batch TEXT,
        technology TEXT,
        total_rounds INTEGER
    )''')

    # Participants
    cur.execute('''CREATE TABLE IF NOT EXISTS participants(
        id INTEGER PRIMARY KEY,
        name TEXT,
        batch TEXT,
        technology TEXT
    )''')

    # Assignments
    cur.execute('''CREATE TABLE IF NOT EXISTS assignments(
        id INTEGER PRIMARY KEY,
        participant TEXT,
        evaluator TEXT,
        technology TEXT,
        round INTEGER
    )''')

    # Evaluation
    cur.execute('''CREATE TABLE IF NOT EXISTS evaluation(
        id INTEGER PRIMARY KEY,
        participant TEXT,
        evaluator TEXT,
        technology TEXT,
        round INTEGER,
        score INTEGER,
        feedback TEXT
    )''')

    # ✅ Insert default users (ADMIN + EVALUATOR)
    cur.execute("SELECT * FROM users WHERE email='admin@gmail.com'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                    ("Admin", "admin@gmail.com", "admin123", "ADMIN"))

    cur.execute("SELECT * FROM users WHERE email='eval@gmail.com'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                    ("Evaluator", "eval@gmail.com", "eval123", "EVALUATOR"))

    conn.commit()
    conn.close()