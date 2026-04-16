import sqlite3

# connects to db or creates it if it doesn't exist
def get_connection():
    conn = sqlite3.connect('./data/creature.db')
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    # create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS creature (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            age INTEGER NOT NULL DEFAULT 0,
            energy INTEGER NOT NULL DEFAULT 100,
            fullness INTEGER NOT NULL DEFAULT 100,
            happiness INTEGER NOT NULL DEFAULT 100,
            memory_json TEXT NOT NULL DEFAULT '[]',
            known_tricks_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL,
            last_interaction TEXT NOT NULL,
            last_decay_check TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()