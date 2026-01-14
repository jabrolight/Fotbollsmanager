from sqlite3 import *

conn = connect("lagen.db")      #skapar en connection till filen, skapar om den inte finns
cursor= conn.cursor()           #skapar en cursor, det som skickar SQL kommmandon

# 1. Rensa bort gammal skit (Bara för testfasen!)
#cursor.execute("DROP TABLE IF EXISTS lagen")

#skapar en tabell med namnet lagen och gör kolumner för lagattribut
cursor.execute("""CREATE TABLE IF NOT EXISTS lagen (lagnamn TEXT PRiMARY KEY, vinster INTEGER, oavgjorda INTEGER, förluster INTEGER, gjorda_mål INTEGER, insläppta_mål INTEGER)""")
#primary key gör så att man inte kan insert ett till lag med samma namn

#fyller en rad i tabellen lagen med en rad för arsenal
cursor.execute("INSERT INTO lagen VALUES(?,?,?,?,?,?)", ("Arsenal", 10, 15, 1, 65, 57))

conn.commit()       #sparar ändringarna

cursor.execute("SELECT * FROM lagen")
tabell= cursor.fetchall()

for lag in tabell:
    print(lag)

conn.close()