import sqlite3

from models import Session


def get_db_connection():
    conn = sqlite3.connect('sessions.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            start_time TEXT,
            user_agent TEXT,
            ip TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_session(session: Session):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessions (session_id, start_time, user_agent, ip) 
        VALUES (?, ?, ?, ?)
    ''', (session.session_id, session.start_time, session.user_agent, session.ip))
    conn.commit()
    conn.close()


def remove_session(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()


def delete_all_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()


def get_all_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    sessions = cursor.execute('SELECT * FROM sessions').fetchall()
    conn.close()
    return [dict(session) for session in sessions]
