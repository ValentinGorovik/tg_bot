import sqlite3
c=sqlite3.connect("heroes.db").cursor()
c.execute("SELECT * FROM heroes")
print("heroes:", c.fetchall())
