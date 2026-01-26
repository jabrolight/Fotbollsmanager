from tkinter import *

class GUI:
    def __init__(self, root, liga):                 #tar ett Liga objekt och ett fönster
        self.liga= liga
        self.root= root


        self.root.geometry("800x750")
        self.root.title("Fotbollsserie")
        #self.huvud_frame()

        self.onboarding_frame= Frame(self.root)
        self.onboarding_frame.pack()
        hälsning= Label(self.onboarding_frame, text="Välkommen! Välj liga", font=("Arial", 40, "bold"), pady=50)
        hälsning.pack()

        demo_knapp= Button(self.onboarding_frame, text="Premier league (testa programmet)", font=(25), width=35, command= self.huvud_frame)
        demo_knapp.pack(padx=25, pady=25)

        skapa_liga_knapp= Button(self.onboarding_frame, text="Skapa en ny liga", font=(25), width= 35)
        skapa_liga_knapp.pack(padx=25, pady=25)

        egna_ligor_knapp= Button(self.onboarding_frame, text="bläddra bland egna ligor", font=("25"), width= 35)
        egna_ligor_knapp.pack(padx=25, pady=25)

        avsluta_knapp= Button(self.onboarding_frame, text="Avsluta", font=(25), width=35, command=self.avsluta)                                       #avsluta körs bid tryck
        avsluta_knapp.pack(padx=25, pady=25)


    def huvud_frame(self):
        self.onboarding_frame.pack_forget()
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
        self.historik.delete(1.0, END)              #tar bort all historik 
        utskrift="matchhistorik: \n"
        historik_lista= self.liga.hämta_historik()      #hämtar senaste historiken
        for match in historik_lista:
            utskrift += f"{match[0]} {match[2]} - {match[3]} {match[1]}\n"
        self.historik.insert(END, utskrift)                         #lägger in den senaste historiken

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