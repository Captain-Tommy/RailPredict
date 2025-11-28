import sqlite3
import os

DB_PATH = "railway_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Trains table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trains (
        train_number TEXT PRIMARY KEY,
        train_name TEXT,
        source TEXT,
        destination TEXT,
        avg_speed TEXT,
        coach_composition TEXT,
        image_url TEXT
    )
    ''')
    
    # Schedules table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_number TEXT,
        station_code TEXT,
        station_name TEXT,
        arrival_time TEXT,
        departure_time TEXT,
        distance TEXT,
        day_count INTEGER,
        FOREIGN KEY (train_number) REFERENCES trains (train_number)
    )
    ''')
    
    # Availability/Waitlist History table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_number TEXT,
        journey_date DATE,
        class_code TEXT,
        quota TEXT,
        current_status TEXT,
        booking_status TEXT,
        scrape_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (train_number) REFERENCES trains (train_number)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
