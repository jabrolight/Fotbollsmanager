"""footbollmanager

inte längre skolprojekt, mitt första riktiga egna projekt

nuvarande steg: förstå och börja med SQL, SQLite och SQLite3
vad jag vet nu: *denna fil ska skrivas om med SQLlite3      *textfilen ska ersättas med en .db fil som är en SQLite fil        *SQL är språket som dessa kommunicerar med

nästa steg: *bättre UI förmodligen customtkinter, kanske pyqt6
*bättre/ proffsig GUI struktur

senast: databas_tabeller() som initierar en tabell (inte den andra än)
introducerat matchhistorik
integrerat uppdatera_db i dokumentera_match2
introducerat matchhistorik i GUI men går att göra bättre med treeview och sedan customtkinter

till nästa gång: hämta rullgardinsmeny istället för text för lagnamn

lär dig treeview för tex att visa matchhistoriken
initiera även andra tabellen, CREATE IF NOT EXISTS


"""

from tkinter import *
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



class GUI:
    def __init__(self, root, liga):                 #tar ett Liga objekt och ett fönster
        self.liga= liga
        self.root= root


        self.root.geometry("800x750")
        self.root.title("Fotbollsserie")

        self.main_frame = Frame(self.root)                      #tydligen bättre stil att ha en main frame än att direkt fylla roten
        self.main_frame.pack()          
        label= Label(self.main_frame, text="välj ett alternativ", font=("Arial",40, "bold"), pady="50")
        label.pack()

        dokumentera_match_knapp= Button(self.main_frame, text="Dokumentera match", font=(25), width=20, command=self.dokumentera_match)         #dokumentera_match körs vid tryck
        dokumentera_match_knapp.pack(padx=25, pady=25)

        se_tabell_knapp= Button(self.main_frame, text="Se tabell", font=(25), width=20, command= self.se_tabell)                                #se_tabell körs vid tryck       
        se_tabell_knapp.pack(padx=25, pady=25)

        avsluta_knapp= Button(self.main_frame, text="Avsluta", font=(25), width=20, command=self.avsluta)                                       #avsluta körs bid tryck
        avsluta_knapp.pack(padx=25, pady=25)    

    def dokumentera_match(self):                                         # fyller en frame med widgets för att dokumentera en match
        self.main_frame.pack_forget()
        self.aktiv_frame = Frame(self.root)                           # en ny frame som knapparna från main frame fyller med olika grejer (här och i se_tabell)
        self.aktiv_frame.pack()                 

        self.hemmalag_var= StringVar()                                                                                #stringvar för att det ska bli smidigare att set() senare (från rullgardinen)
        self.hemmalag_var.set("Välj hemmalag")
        self.hemmalag_label = Label(self.aktiv_frame, text="Hemmalag: ", font=(25))
        self.hemmalag_label.grid(column=1, row=1)
        self.hemmalag_inmatning= OptionMenu(self.aktiv_frame, self.hemmalag_var, *self.liga.alla_lagnamn())
        self.hemmalag_inmatning.grid(column= 1, row=2, padx=20, pady=20)

        self.bortalag_var= StringVar()
        self.bortalag_var.set("Välj bortalag")
        self.bortalag_label= Label(self.aktiv_frame, text="Bortalag: ", font=(25))
        self.bortalag_label.grid(column=3, row=1)
        self.bortalag_inmatning= OptionMenu(self.aktiv_frame, self.bortalag_var, *self.liga.alla_lagnamn())
        self.bortalag_inmatning.grid(column= 3, row=2, padx=20, pady=20)

        self.hemmalag_mål_label= Label(self.aktiv_frame, text="Hemmalagets mål", font=(25))
        self.hemmalag_mål_label.grid(column=1, row=3)
        self.hemmalag_mål_inmatning= Entry(self.aktiv_frame)
        self.hemmalag_mål_inmatning.grid(column=1, row=4)

        streck= Label(self.aktiv_frame, text="-", font=(25))
        streck.grid(column=2, row=3)

        self.bortalag_mål_label= Label(self.aktiv_frame, text="Bortalagets mål", font=(25))
        self.bortalag_mål_label.grid(column=3, row=3)
        self.bortalag_mål_inmatning= Entry(self.aktiv_frame)
        self.bortalag_mål_inmatning.grid(column=3, row=4)

        spara_knapp= Button(self.aktiv_frame, text= "Spara", font=(25), width=20, command=self.spara_match)                         #knappen som sätter igång hanteringen av all inmatning
        spara_knapp.grid(column=2, row=5, pady=30)

        tillbaka_knapp = Button(self.aktiv_frame, text="tillbaka", font=(25), width=20, command= self.tillbaka_knapp)               #för att gå tillbaka till main frame
        tillbaka_knapp.grid(column=2, row=6, pady=30)

        self.historik= Text(self.aktiv_frame, width=50, height=10)
        self.historik.grid(column=1, row=12, columnspan=3)

        self.visa_historik()


    def spara_match(self):
        self.felmeddelande= Label(self.aktiv_frame, text="", font=(25), width=40, height=3)       # height=3 för att täcka ett föregående meddelande som är två rader
        self.felmeddelande.grid(column=2, row=7)                                                                                         #det är samma felmeddalande som används i hela programmet, bara texten ändras

        try:
            hemmamål= int(self.hemmalag_mål_inmatning.get())
            bortamål= int(self.bortalag_mål_inmatning.get())
        except ValueError:
            self.felmeddelande.config(text="fel inmatning, skriv resultatet i siffror")
            return
        
        if self.hemmalag_var.get()== "Välj hemmalag" or self.bortalag_var.get()== "Välj bortalag":
            self.felmeddelande.config(text="Välj både hemma och bortalag")
            return
        
        if self.hemmalag_var.get() == self.bortalag_var.get():
            self.felmeddelande.config(text="Ett lag kan inte möta sig sjäkv")
            return

        #kontrollerna över gör så att man alltid hamnar här till slut
        self.liga.dokumentera_match2(self.hemmalag_var.get(), self.bortalag_var.get(), hemmamål, bortamål)                    # dokumentera_match2 anropar i sin tur spelad_match för att ändra Lag attribut

        self.felmeddelande.config(text=" ")
        skriv_ut = Label(self.aktiv_frame, text=f"matchen {self.hemmalag_var.get()}-{self.bortalag_var.get()}\n{hemmamål}-{bortamål} registrerad", font=(25), width=40)       #bekräftar att allt har kontrollerats
        skriv_ut.grid(column=2, row=11, pady=10)

        self.visa_historik()

    
    def visa_historik(self):
        self.historik.delete(1.0, END)
        utskrift="matchhistorik: \n"
        historik_lista= self.liga.hämta_historik()
        for match in historik_lista:
            utskrift += f"{match[0]} {match[2]} - {match[3]} {match[1]}\n"
        self.historik.insert(END, utskrift)

    def se_tabell(self):                                #visar tabellen i en sekundär frame
        self.main_frame.pack_forget()
        self.aktiv_frame = Frame(self.root)
        self.aktiv_frame.pack()                           

        tabell= Label(self.aktiv_frame, text=self.liga, font=("Courier", 11), justify=LEFT)     #courier används för att alla tecken är lika stora, tabellen blir rak
        tabell.pack()          

        tillbaka_knapp = Button(self.aktiv_frame, text="tillbaka", font=(25), width=20, command= self.tillbaka_knapp)
        tillbaka_knapp.pack(padx=25, pady=25)

    def tillbaka_knapp(self):               #det som alltid anropas när man klickar på tillbaka knappen, förstör den tillfäliga framen (aktiv.frame) och visar main igen
        self.aktiv_frame.destroy()
        self.main_frame.pack()


    def avsluta(self):              #avslutar programmet
        self.root.destroy()
    

     

def main():
    premier_league= Liga("Lagen.db")
    root= Tk()
    GUI(root, premier_league)
    root.mainloop()

main()
    

