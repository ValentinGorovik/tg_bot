import sqlite3

DB = "heroes.db"

def show_all():
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Таблицы:", tables)
    print("\nДанные в heroes:")
    cur.execute("SELECT id, nick, gender, race, created_at FROM heroes;")
    rows = cur.fetchall()
    if not rows:
        print("  (пусто)")
    else:
        for row in rows:
            print(" ", row)
    conn.close()

if __name__ == "__main__":
    show_all()
