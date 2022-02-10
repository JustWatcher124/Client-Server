import tkinter as tk
from tkinter import ttk
from nachrichtFormatter import *
from socketLib import *
import auswahlGui
# Chat Fenster mit Nachrichteneingabe


# Funktion zum Befüllen des Fensters mit den Widgets
def gui(fenster):
    global window
    window = fenster
    toprow = tk.Frame(window, height=50)
    chatverlauf = tk.Canvas(window, bg="#D3D3D3",height=250)
    kein_verlauf = tk.Label(toprow,text="Es sind keine Nachrichten vorhanden, drücke auf 'refresh'",width=50)
    tk.Button(toprow, text="Zurück", command=back_to_Auswahl).grid(row=0,column=0)
    tk.Button(toprow,text="Schließen",command= chatSchliessen).grid(row=0,column=2)
    tk.Button(toprow,text="Refresh",command= lambda: refresh(kein_verlauf,chatverlauf)).grid(row=0,column=4)
    bottomrow = tk.Frame(window)
    text_input = tk.Text(bottomrow, height = 1, width=50)
    tk.Button(bottomrow,text="Absenden", command= lambda: text_absenden(text_input,kein_verlauf,chatverlauf)).grid(row=2,column=1)
    text_input.grid(row=2,column=0)
    toprow.grid()
    kein_verlauf.grid()
    chatverlauf.grid()
    bottomrow.grid()
    refresh(kein_verlauf,chatverlauf)
    return window

# Funktion des Knopfen "Schließen"
def chatSchliessen():
    global window
    window.destroy()

# Funktion des Knopfes "Zurück"
# Schließt das Chatfenster und öffnet die Chatauswahl wieder
def back_to_Auswahl():
    global nickname, client
    chatSchliessen()
    auswahlGui.starteGui(client,nickname)

# Funktion des Knopfes "Absenden"
# Liest die eingegebene Nachricht und löscht den Inhalt des Textfeldes
def text_absenden(text,k_v,cv):
    global client, neuer_chat
    nachricht = text.get(1.0,"end-1c")
    nachricht_zum_server(nachricht)
    neuer_chat = False
    text.delete("1.0","end-1c")
    refresh(k_v,cv)

# Funktion unter text_absenden()
# schickt dem Server die Nachricht im json-string Format
def nachricht_zum_server(nachricht):
    global nickname, komm_partner
    raw = nachrichtTjson(nickname,komm_partner,nachricht)
    sendeStr(client,"6"+raw); sendeTrennByte(client)


# Funktion unter refresh()
# Löscht den Inhalt eines tk_Frames/Windows
# Damit Nachrichten nicht mehrfach angezeigt werden
def clear_widgets(tk_frame):
    for widget in tk_frame.winfo_children():
        widget.destroy()

# Funktion des Knopfes "Refresh"
# Empfängt den Chatverlauf vom Server und übergibt ihn an make_chatVerlauf()
def refresh(kein_verlauf,chat_verlauf):
    global client, komm_partner, neuer_chat
    clear_widgets(chat_verlauf)
    if not neuer_chat:
        sendeStr(client,"4"+komm_partner)
        sendeTrennByte(client)
        nachricht_raw = empfangeStr(client)
        nachricht = verlaufToJson(nachricht_raw[1:])
        kein_verlauf.destroy()
        make_chatVerlauf(chat_verlauf,nachricht)
    else:
        kein_verlauf.config(text="Es gibt keine Nachrichten für diesen Kontakt")

# Funktion unter refresh()
# Um das Layout der Nachrichten zu machen und diese anzuzeigen 
def make_chatVerlauf(anzeige,verlauf_raw):
    global nickname, partner
    if verlauf_raw == '':
        tk.Label(anzeige,text="Es gibt keine Nachrichten!").grid()
    else:
        for message in verlauf_raw:
            mes = ""
            seite = [(0,"#a9a9a9"),(1,"#90ee90")][1 if message["sender"]==nickname else 0]
            n = message["sender"]
            t = message["nachricht"]
            z = message["datum"].split(",")[1]
            d = message["datum"].split(",")[0]
            mes = z+" "+d+" "+n+"\n"+t
            tk.Label(anzeige,text=mes,bg=seite[1]).grid(column=seite[0])


# Anfang des Fensters
# Beinhaltet das Fenster dessen mainloop
def starteGui(client_socket,nick,partner, new_chat):
    global client, nickname, komm_partner, neuer_chat
    client = client_socket
    nickname = nick
    komm_partner = partner
    neuer_chat = new_chat
    app = tk.Tk()
    app.title("Ihr Chat mit:"+komm_partner)
    app = gui(app)
    app.mainloop()


