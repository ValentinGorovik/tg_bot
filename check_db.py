import sqlite3

def show_all():
    conn = sqlite3.connect("heroes.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM heroes;")
    rows = cur.fetchall()
    print("heroes:", rows or "(пусто)")
    conn.close()

if __name__=="__main__":
    show_all()
