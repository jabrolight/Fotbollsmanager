"""nytt i denna version: 
omvandalr 3.2 till OOP

allt är nu case insensitive
checka input finns istället för dubbelkod

** från 3.2 och tidigare: 

följande saker från version 3.0: 
fixar inmatningen av resultat och använder .join för att skriva ut lagen vid fel inmatning
fixat så att den sorterar tabellen innan utskrift
ändrad __lt__ för sortering i flera steg


i 3.1: göra en funktion för kontroll av inmatning istället för att skriva koden dubblet (för hemma och bortalag)

problem på vägen: efter att jag ändrade __lt__ funkade allt som det ska förutom alfabetiska ordningen pga reversed= true
tog nu bort reveresed= true men ändrade < och > i __lt__ istället

en bugg hittad!! man kan välja samma lag som hemma och borta (((LÖST NU!! men while loop i dokumentera_match)))

hur mycket kan jag ändra i A-nivå? kan jag bara låta användaren välja lag från lista istället för att skriva?

separerar logik för att sen bygga GUI runt det, hittils: 
-tagit bort att skriva "meny" tar dig tillbaka till menyn då det finns en tillbaka knapp
- nu returneras None om det inte finns några matchningar med inmatningen
- frågar inte om ny inmatning efter check
"""

from tkinter import *

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
    
    def skriv_lag_i_fil(self):      #vet hur en rad skrivs i filen, Liga.skriv_i_fil använder denna i en loop
        return f"{self.lagnamn};{self.vinster};{self.oavgjorda};{self.förluster};{self.gjorda_mål};{self.insläppta_mål}\n"



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
    def __init__(self, fil):
        self.fil= fil
        self.dict_med_lag = {}
        self.fylla_dict_med_objekt()        #fyller dict direkt, slipper göra det i main
    
    def __str__(self):          #istället för skriv_ut_tabell utanför en klass
        tabell = f"{"V":>20}{"O":>4}{"F":>4}{"M":>7}{"P":>5}\n"
        sorterad_lista = sorted(list(self.dict_med_lag.values()))

        position =1 
        for lag in sorterad_lista:
            tabell += f"{position:<2} {lag}\n"
            position +=1
        return tabell
    
    def fylla_dict_med_objekt(self):        # istället för läs_in_från_fil  #läser in filen och fyller en dictionary med lagnamn som nyckel och Lagobjekt som värde
        with open(self.fil, "r", encoding="utf-8") as fil:
            for rad in fil:
                rad = rad.strip().split(";")
                self.dict_med_lag[rad[0]]= Lag(rad[0], rad[1], rad[2], rad[3], rad[4], rad[5])
        return self.dict_med_lag

    def checka_2(self, lagnamn):                #version 2 av checka_input, fyller en lista med lag som matchar inmatningen, GUI väljer sen hur det ska användas
 
        lagnamn = lagnamn.lower().strip()
        for lag in self.dict_med_lag:
            if lag.strip().lower() == lagnamn:
                return [lag]
                                          
        matchningar= []
        for lag in self.dict_med_lag:
            if lag.lower().startswith(lagnamn):
                matchningar.append(lag)

        return matchningar                      #lista med alla lag som börjar med inmatningen

    def dokumentera_match2(self, hemmalagets_namn, bortalagets_namn, hemmalag_mål, bortalag_mål):           # version 2 av dokumentera_match, förenklad då GUI hanterar resten

        hemmalaget= self.dict_med_lag[hemmalagets_namn]                     # tar lagnamn som redan är 100% korrekta, kontrolleras av GUI via checka_2
        bortalaget= self.dict_med_lag[bortalagets_namn]
        
                                                 
        hemmalaget.spelad_match(hemmalag_mål, bortalag_mål)                 #ändrar Lag-objektens attribut
        bortalaget.spelad_match(bortalag_mål, hemmalag_mål)


    def skriv_i_fil(self):      #vet inte inte en rad skrivs i filen för det finnns i Lag men använder den i en loop
        with open(self.fil, "w", encoding="utf-8") as fil:
            for lag in self.dict_med_lag.values():
                fil.write(lag.skriv_lag_i_fil())


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
        self.hemmalag_label = Label(self.aktiv_frame, text="Hemmalag: ", font=(25))
        self.hemmalag_label.grid(column=1, row=1)
        self.hemmalag_inmatning= Entry(self.aktiv_frame, textvariable= self.hemmalag_var)
        self.hemmalag_inmatning.grid(column= 1, row=2, padx=20, pady=20)

        self.bortalag_var= StringVar()
        self.bortalag_label= Label(self.aktiv_frame, text="Bortalag: ", font=(25))
        self.bortalag_label.grid(column=3, row=1)
        self.bortalag_inmatning= Entry(self.aktiv_frame, textvariable= self.bortalag_var)
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

    def spara_match(self):
        self.felmeddelande= Label(self.aktiv_frame, text="", font=(25), width=40, height=3)       # height=3 för att täcka ett föregående meddelande som är två rader
        self.felmeddelande.grid(column=2, row=7)                                                                                         #det är samma felmeddalande som används i hela programmet, bara texten ändras
        self.meny= StringVar(self.aktiv_frame, value="Välj här")        #används för en rullgardinsmeny vid fel inmatning

        hemmalag= self.hemmalag_inmatning.get()                                           
        bortalag= self.bortalag_inmatning.get()
        try:
            hemmamål= int(self.hemmalag_mål_inmatning.get())
            bortamål= int(self.bortalag_mål_inmatning.get())
        except ValueError:
            self.felmeddelande.config(text="fel inmatning, skriv resultatet i siffror")
            return

        inmatningsmatchning_hemmalag= self.liga.checka_2(hemmalag)                                  #anropar check_2 för att få tillbaka en lista
        inmatningsmatchning_bortalag= self.liga.checka_2(bortalag)

        if len(inmatningsmatchning_hemmalag)==0:                                                                   #hanterar listan från checka_2 beroende på längd (hemma, sen bortalaget)
            self.felmeddelande.config(text=f"det finns inget lag som heter {hemmalag}")
            return
        elif len(inmatningsmatchning_hemmalag)>1:
            self.felmeddelande.config(text=f"Du skrev {hemmalag}, vilket av dessa lag menar du? \n {inmatningsmatchning_hemmalag}")
            rullgardin_med_matchningar= OptionMenu(self.aktiv_frame, self.meny, *inmatningsmatchning_hemmalag)                              # "*" gör så att varje element i listan blir ett alternativ i rullgardinen
            rullgardin_med_matchningar.grid(column=2, row=9)
            välj_knapp= Button(self.aktiv_frame, text="välj", width=20, command=lambda: self.välj_från_rullgardin("Hemmalaget") )                 #anropar välj_från_rullgardin som bekräftar användarens val
            välj_knapp.grid(column=2, row=10, pady=10)
            return
        
        if len(inmatningsmatchning_bortalag)==0:
            self.felmeddelande.config(text=f"det finns inget lag som heter {bortalag}")
            return
        elif len(inmatningsmatchning_bortalag)>1:
            self.felmeddelande.config(text=f"Du skrev {bortalag}, vilket av dessa lag menar du? \n {inmatningsmatchning_bortalag}")
            rullgardin_med_matchningar= OptionMenu(self.aktiv_frame, self.meny, *inmatningsmatchning_bortalag )
            rullgardin_med_matchningar.grid(column=2, row=9)
            välj_knapp= Button(self.aktiv_frame, text="välj", width=20, command=lambda: self.välj_från_rullgardin("Bortalaget") )
            välj_knapp.grid(column=2, row=10, pady=10)
            return
        
        

        if len(inmatningsmatchning_hemmalag)==1 and len(inmatningsmatchning_bortalag)==1:               #om användaren skriver rätt lagnamn eller med bara ett lag som kan ha menats
            hemmalagets_namn= inmatningsmatchning_hemmalag[0]
            bortalagets_namn= inmatningsmatchning_bortalag[0]
            if hemmalagets_namn== bortalagets_namn:
                self.felmeddelande.config(text="Ett lag kan inte möta sig själv")
                return
            #kontrollerna över gör så att man alltid hamnar här till slut
            self.liga.dokumentera_match2(hemmalagets_namn, bortalagets_namn, hemmamål, bortamål)                    # dokumentera_match2 anropar i sin tur spelad_match för att ändra Lag attribut

        self.felmeddelande.config(text=" ")
        skriv_ut = Label(self.aktiv_frame, text=f"matchen {hemmalagets_namn}-{bortalagets_namn}\n{hemmamål}-{bortamål} registrerad", font=(25), width=40)       #bekräftar att allt har kontrollerats
        skriv_ut.grid(column=2, row=11, pady=10)

        self.liga.skriv_i_fil()                                  #uppdaterar filen

    def välj_från_rullgardin(self, hemma_eller_borta):              #har parametern hemma_eller_borta för att avgöra vilket lag valet från rullgardinen berör
        valet= self.meny.get()
        if hemma_eller_borta == "Hemmalaget":
            self.hemmalag_var.set(valet)
        elif hemma_eller_borta =="Bortalaget":
            self.bortalag_var.set(valet)

        self.spara_match()                              #går tillbaka till spara_match för att fånga andra fel eller köra igenom hela
 

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
    premier_league= Liga("Lagfil.txt")
    root= Tk()
    GUI(root, premier_league)
    root.mainloop()

main()
    

