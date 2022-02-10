import tkinter as tk
nickname = ""
# Erstes Fenster das sich öffnet wenn ein Client sich öffnet


# Main Funktion, Startet das Fenster
# gibt am Ende den gewählten Namen zurück
def main():
    global nickname
    chat = tk.Tk()
    chat.title("Chat")
    chat = initNickFenster(chat)
    chat.mainloop()
    return nickname


# Funktion zur Befüllung des Fensters
def initNickFenster(gui):
    global window
    window = gui
    l = tk.Label(window,text="""Bitte geben Sie einen Benutzernamen ein.\n
    (Ohne Leerzeichen und Komma)""").grid()
    nick_in = tk.Text(window,height = 1, width =45)
    # Error Label e, um Anzuzeigen wenn der Name nicht gut ist
    e = tk.Label(window,text="")
    nick_in.grid(row=1,column=0)
    tk.Button(window,text="Fertig",command= lambda: goodNick(nick_in,e)).grid(row=1,column=1)
    e.grid(row=2)
    #tk.Button(window,text="Standard", command=standard).grid()
    window.grid()
    return gui


# Funktion um den Standardnamen zu übernehmen (vereinfachung zum Testen)
# In der Abgabe nicht "Aktiviert";
# Zum Aktivieren die kommentierte Zeile in initNickFenster wieder auskommentieren
def standard():
    global nickname, window
    nickname = "JustWatcher124"
    window.destroy()


# Funktion zum Überprüfen ob der Name Leerzeichen, Kommas beinhält oder Leer ist
# Funktion des Knopfes "Fertig"
def goodNick(text,error):
    global nickname, window
    name = text.get(1.0,"end-1c")
    if " " in name or "," in name or name == "":
        error.config(text="Unzulässiger Name")
    else:
        nickname = name
        print(nickname)
        window.destroy()

