import sqlite3

DB_PATH = "railway_data.db"

def migrate_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE trains ADD COLUMN avg_speed TEXT")
        print("Added avg_speed column.")
    except sqlite3.OperationalError:
        print("avg_speed column already exists.")
        
    try:
        cursor.execute("ALTER TABLE trains ADD COLUMN coach_composition TEXT")
        print("Added coach_composition column.")
    except sqlite3.OperationalError:
        print("coach_composition column already exists.")
        
    try:
        cursor.execute("ALTER TABLE trains ADD COLUMN image_url TEXT")
        print("Added image_url column.")
    except sqlite3.OperationalError:
        print("image_url column already exists.")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_db()
