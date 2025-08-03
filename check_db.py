import sqlite3
DB = "heroes.db"
c  = sqlite3.connect(DB).cursor()
c.execute("SELECT * FROM heroes")
print("heroes:", c.fetchall() or "(пусто)")
