from sqlite3 import *

class Lag: 
    def __init__(self, lagnamn, vinster, oavgjorda, förluster, gjorda_mål, insläppta_mål):
        self.lagnamn= lagnamn
        self.vinster=int(vinster)
        self.oavgjorda=int(oavgjorda)
        self.förluster= int(förluster)
        self.gjorda_mål= int(gjorda_mål)
        self.insläppta_mål= int(insläppta_mål)
        self.poäng= int(oavgjorda)+int(vinster)*3       #poäng beräknas av andra attribut och behöver därför inte heller lagras i filen

    def __str__(self):      #objekten skrivs ut som en rad av tabellen, används i Liga.__str__
        return f"{self.lagnamn:<15} {self.vinster:<3} {self.oavgjorda:<3} {self.förluster:<3} {self.gjorda_mål:>3}-{self.insläppta_mål:<3} {self.poäng:<3}" 
    

    def __lt__(self, other):                #flera steg för jämförelser, går till nästa endast om steget över är lika 
        if self.poäng != other.poäng:
            return self.poäng > other.poäng   
        elif self.gjorda_mål - self.insläppta_mål != other.gjorda_mål - self.insläppta_mål :
            return self.gjorda_mål - self.insläppta_mål > other.gjorda_mål - self.insläppta_mål
        elif self.gjorda_mål != other.gjorda_mål:
            return self.gjorda_mål > other.gjorda_mål
        else: 
            return self.lagnamn < other.lagnamn 
    
    def spelad_match(self, mål_för, mål_emot):      # ändrar attribut efter ett registrerat matchresultat
        self.gjorda_mål += mål_för
        self.insläppta_mål += mål_emot
        if mål_för > mål_emot:
            self.vinster +=1
            self.poäng +=3
        elif mål_för == mål_emot:
            self.oavgjorda += 1
            self.poäng +=1
        elif mål_för < mål_emot:
            self.förluster += 1



        

class Liga():
    def __init__(self, ligafil):
        self.fil= ligafil
        self.dict_med_lag = {}
        self.databas_tabeller()             #skapar tabellerna om dem inte redan finns
        self.fylla_dict_med_objekt()        #fyller dict direkt, slipper göra det i main



    def __str__(self):          #istället för skriv_ut_tabell utanför en klass
        tabell = f"{"V":>20}{"O":>4}{"F":>4}{"M":>7}{"P":>5}\n"
        sorterad_lista = sorted(list(self.dict_med_lag.values()))

        position =1 
        for lag in sorterad_lista:
            tabell += f"{position:<2} {lag}\n"
            position +=1
        return tabell
    
    def databas_tabeller(self):
        conn= connect(self.fil)
        cursor= conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS lagen (lagnamn TEXT PRIMARY KEY, vinster INTEGER, oavgjorda INTEGER, förluster INTEGER, gjorda_mål INTEGER, insläppta_mål INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS matchhistorik (match_id INTEGER PRIMARY KEY AUTOINCREMENT, hemmalag TEXT, bortalag TEXT, hemmamål INTEGER, bortamål INTEGER)")

        conn.commit()
        conn.close()

    def fylla_dict_med_objekt(self):        #hämtar datan från db och fyller dict
        conn= connect(self.fil)     
        Cursor= conn.cursor()
        Cursor.execute("SELECT * FROM lagen")
        lista_med_lag= Cursor.fetchall()            #lägger allt från db i en lista

        for lag in lista_med_lag:
            self.dict_med_lag[lag[0]]= Lag(*lag)        # *lag funkar istället för lag[0], lag[1], lag[2]... för att databasen har samma kolumnordning som Laagattributen
        conn.close()
        return self.dict_med_lag


    def dokumentera_match2(self, hemmalagets_namn, bortalagets_namn, hemmalag_mål, bortalag_mål):           # version 2 av dokumentera_match, förenklad då GUI hanterar resten

        hemmalaget= self.dict_med_lag[hemmalagets_namn]                     # tar lagnamn som redan är 100% korrekta, kontrolleras av GUI via checka_2
        bortalaget= self.dict_med_lag[bortalagets_namn]
        
                                                 
        hemmalaget.spelad_match(hemmalag_mål, bortalag_mål)                 #ändrar Lag-objektens attribut
        bortalaget.spelad_match(bortalag_mål, hemmalag_mål)

        with connect(self.fil) as conn:
            cursor= conn.cursor()
            cursor.execute("UPDATE lagen SET vinster=?, oavgjorda=?, förluster=?, gjorda_mål=?, insläppta_mål=? WHERE lagnamn=?", (hemmalaget.vinster, hemmalaget.oavgjorda, hemmalaget.förluster, hemmalaget.gjorda_mål, hemmalaget.insläppta_mål, hemmalaget.lagnamn))
            #uppdaterar hemmalaget i db
            cursor.execute("UPDATE lagen SET vinster=?, oavgjorda=?, förluster=?, gjorda_mål=?, insläppta_mål=? WHERE lagnamn=?", (bortalaget.vinster, bortalaget.oavgjorda, bortalaget.förluster, bortalaget.gjorda_mål, bortalaget.insläppta_mål, bortalaget.lagnamn))
            #uppdaterar bortalaget i db
            cursor.execute("INSERT INTO matchhistorik(hemmalag, bortalag, hemmamål, bortamål) VALUES(?,?,?,?)", (hemmalagets_namn, bortalagets_namn, hemmalag_mål, bortalag_mål))
            #lägger till matchen i historiken
            conn.commit()

    def hämta_historik(self):
        with connect(self.fil) as conn:
            Cursor=conn.cursor()
            Cursor.execute("SELECT hemmalag, bortalag, hemmamål, bortamål FROM matchhistorik ORDER BY match_id DESC")
            historik= Cursor.fetchall()
        return historik
    

    def alla_lagnamn(self):
        lista_med_lagnamn=[]                    #används för rullgardinen i GUI
        for lagnamn in self.dict_med_lag.keys():
            lista_med_lagnamn.append(lagnamn)
        return lista_med_lagnamn

    def demodata(self):                 #anropas om användaren att köra demo istället för att skapa en egen liga
        demolag= [("Arsenal",0,0,0,0,0) ,("Man City",0,0,0,0,0) ,("Chelsea",0,0,0,0,0) ,("Aston Villa",0,0,0,0,0) ,("Brighton",0,0,0,0,0),
                ("Sunderland",0,0,0,0,0) ,("Man Utd",0,0,0,0,0) ,("Liverpool",0,0,0,0,0) ,("Crystal Palace",0,0,0,0,0) ,("Brentford",0,0,0,0,0),
                ("Bournemouth",0,0,0,0,0) ,("Tottenham",0,0,0,0,0) ,("Newcastle",0,0,0,0,0) ,("Everton",0,0,0,0,0) ,("Fullham",0,0,0,0,0),
                ("Nottingham",0,0,0,0,0) ,("West Ham",0,0,0,0,0) ,("Leeds",0,0,0,0,0) ,("Burnkey",0,0,0,0,0) ,("Wolverhampton",0,0,0,0,0)]
        with connect(self.fil) as conn:
            cursor= conn.cursor()
            cursor.execute("DELETE FROM lagen")     #rensar tabellen efter varje demo
            cursor.executemany("INSERT INTO lagen VALUES(?,?,?,?,?,?)", demolag)    #fyller demoligan
            conn.commit()

    def skapa_egen_liga(self, liganamn: str, laglista: list):      #dessa kommer från GUI
        if not liganamn.isalnum():
            return False            #säg åt användaren att bara använda bokstäver och siffror (inte mellanslag)
        with connect(self.fil)as conn:
            cursor=conn.cursor()
            cursor.execute(f"SELECT name FROM SQLITE_MASTER WHERE type='table' AND name=?", (liganamn,))
            tabellnamn= cursor.fetchone()
            if tabellnamn is None:

                cursor.execute(f"CREATE TABLE {liganamn} (lagnamn TEXT PRIMARY KEY, vinster INTEGER, oavgjorda INTEGER, förluster INTEGER, gjorda_mål INTEGER, insläppta_mål INTEGER)")

                for lag in laglista:
                    cursor.execute(f"INSERT INTO {liganamn} VALUES (?,?,?,?,?,?)", (lag,0,0,0,0,0))
            
                return True
            else:
                return 0 #returnerar inte false för att det görs längre upp, två false hade gjort så att GUI inte vet var felet är
            
    

            
