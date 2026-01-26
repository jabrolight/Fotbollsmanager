from backend import Liga
from GUI import *

def main():
    premier_league= Liga("Lagen.db")
    root= Tk()
    GUI(root, premier_league)
    root.mainloop()

main()