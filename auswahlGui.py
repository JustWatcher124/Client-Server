import tkinter as tk
from nachrichtFormatter import *
from functools import partial
from socketLib import *
import chatGui
chat_partner = ""




# Funktion um das Fenster "Chatauswahl" zu generieren
# Das Fenster und die möglichen Chatpartner werden gegeben; Das Fenster (fenster) wird befüllt mit unter anderem den Chatpartnern (names)
# Zurückgegeben wird das befüllte Fenster, wo alle Knöpfe und Funktionen hinterlegt sind
def gui(fenster,names):
    global window
    window = fenster
    toprow = tk.Frame(window,bg="#A9A9A9")
    bottomrow = tk.Frame(window)
    partners = tk.Frame(window)
    partners = refresh(partners,names)
    # Knopf um das Fenster und den Client zu Schließen
    tk.Button(toprow,text="Schließen",command= guiSchliessen).grid(row=0,column=0)
    # Knopf um vom verbundenen Server die möglichen Chatpartner upzudaten
    tk.Button(toprow,text="Refresh",command= lambda: refresh(partners,get_Komm_Partner())).grid(row=0,column=2)
    tk.Label(bottomrow,text="Hier können Sie einen neuen Chatpartner angeben").grid()
    neuer_chat = tk.Text(bottomrow,width = 50, height = 1)
    er_neuer_chat = tk.Label(bottomrow,text="")
    tk.Button(bottomrow,text="Chat Beginnen",
    command= lambda: chat_beginnen(neuer_chat,er_neuer_chat)
    ).grid(row=1,column=1)
    neuer_chat.grid(row=1,column=0)
    er_neuer_chat.grid(row=2)
    toprow.pack(side="top")
    partners.pack()
    bottomrow.pack(side="bottom")
    return window

# Funktion des Knopfes "Chat Beginnen"
# Gibt dem chat_partner einen neuen Wert aus dem Eingabefeld
def chat_beginnen(nc,er_nc):
    global window, chat_partner
    name = nc.get(1.0,"end-1c")
    if " " in name or "," in name:
        er_nc.config(text="Unzulässiger Name")
    else:
        chat_partner = name
        print("Neuer Chat mit:",chat_partner)
        window.destroy()

# Gibt die möglichen Kommunikationspartner in einem String zurück
# Arbeitet mit der Socket
def get_Komm_Partner():
    global client
    sendeStr(client,"2"); sendeTrennByte(client)
    raw = empfangeStr(client)
    return getKommPartner(raw[1:])


# Funktion um alle Elemente innerhalb eines Frames/Fenster zu löschen
# programm schreibt ansonsten immer das gleiche immer wieder in das Fenster
def clear_widgets(tk_frame):
    for widget in tk_frame.winfo_children():
        widget.destroy()

# Funktion des Knopfes "Refresh"
# Updatet die Knöpfe mit den bekannten Chatpartnern 
def refresh(partners,names):
    global name_liste#, btn_liste
    name_liste = names
    clear_widgets(partners)
    if len(names)>0:
        for partner in names:
            x = "chat_Aufruf(\""+str(partner)+"\")"
            btn = tk.Button(partners,text=partner, command=partial(chat_Aufruf, str(partner.split()[0])))
            btn.pack()
            print(btn)

    else:
        tk.Label(partners,text="Sie haben keine Chatverläufe!").pack()
    return partners


# Funktion um das Fenster zu Schliessen bevor der mainloop fertig ist
# Funktion des Knopfes "Schließen"
def guiSchliessen():
    global window
    window.destroy()


# Funktion jedes Knopfes, jedes bekannten Chatpartners
# Schließt das Fenster und gibt dem ChatPartner den Wert des Knopfes
def chat_Aufruf(name):
    global window, chat_partner
    chat_partner = name
    print("Chat mit",chat_partner," aufgerufen")
    window.destroy()


    
# Funktion um das Fenster zu generieren und in den nächsten Schritt zu gehen (siehe chatGui.py)
def starteGui(client_socket,nick):
    global client, nickname, chat_partner, new_chat
    client = client_socket
    nickname = nick
    app = tk.Tk()
    partner = get_Komm_Partner()
    app.title("Chatauswahl")
    app = gui(app,partner)
    app.mainloop()
    if chat_partner != "":
        chatGui.starteGui(client,nickname,chat_partner,False)

