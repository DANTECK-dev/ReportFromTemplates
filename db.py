import psycopg2
from psycopg2 import sql
import os

DB_NAME = os.getenv("POSTGRES_DB", "test_db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            university TEXT,
            student_name TEXT,
            group_name TEXT,
            course TEXT,
            department TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def user_exists(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def add_user(telegram_id, university, student_name, group_name, course, department):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, university, student_name, group_name, course, department)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (telegram_id) DO NOTHING
    """, (telegram_id, university, student_name, group_name, course, department))
    conn.commit()
    cursor.close()
    conn.close()
