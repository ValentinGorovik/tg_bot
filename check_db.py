import sqlite3
con = sqlite3.connect("heroes.db")
rows = con.execute("SELECT * FROM heroes").fetchall()
print("heroes:", rows or "(пусто)")
con.close()
