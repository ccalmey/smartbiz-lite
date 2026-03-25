#SMARTBIZ MVP 
#SYSTEM DEVELOPER: CALMEY CROWN @rown.calmey 
#START DATE: 3.12.2025
#UPDATE: 31.12.2025

# init_db.py
# SMARTBIZ LITE ¡ª Database Initialization


from db import get_db_connection

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL,
            deleted INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL,
            deleted INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
    print("[!] Database initialized successfully")

if __name__ == "__main__":
    init_db()
