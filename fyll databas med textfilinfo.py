from sqlite3 import *

conn= connect("Lagen.db")
cursor= conn.cursor()
cursor.execute("DROP TABLE IF EXISTS lagen")

cursor.execute("""CREATE TABLE IF NOT EXISTS lagen (lagnamn TEXT PRIMARY KEY, vinster INTEGER, oavgjorda INTEGER, förluster INTEGER, gjorda_mål INTEGER, insläppta_mål INTEGER)""")

with open("Lagfil.txt", "r", encoding="utf-8") as fil:
    for rad in fil:
        rad = rad.strip().split(";")
        cursor.execute("INSERT OR IGNORE INTO lagen VALUES(?,?,?,?,?,?)", (rad[0], int(rad[1]), int(rad[2]), int(rad[3]), int(rad[4]), int(rad[5])))

conn.commit()

cursor.execute("SELECT * FROM lagen")
tabell= cursor.fetchall()
for lag in tabell:
    print(lag)

conn.close()


