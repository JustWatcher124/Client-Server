import tkinter as tk
from nachrichtFTjson import *
from socketLib import *


def gui(fenster,names):
    global window
    window = fenster
    toprow = tk.Frame(window,bg="#A9A9A9")
    bottomrow = tk.Frame(window)
    tk.Button(toprow,text="Schließen",command= guiSchliessen).grid(row=0,column=0)
    tk.Button(toprow,text="refresh",command= lambda: refresh(verlauf)).grid(row=0,column=2)
    partners = tk.frame(window)
    if len(partner)>0:
        for partner in names:
            tk.Button(partners,text=partner, command= lambda: chat_Aufruf(partner)).pack()
    else:
        tk.Label(text="Sie haben keine Chatverläufe!")
    neuer_chat = tk.Text(bottomrow,width = 50).grid(column=0)
    chat_beginnen = tk.Button(bottomrow,text="Chat Beginnen").grid(column=1)
    toprow.pack(side="top")
    chatverlauf.pack()
    bottomrow.pack(side="bottom")
    return window


def get_Komm_Partner():
    global client
    sendeStr(client,"2"); sendeTrennByte(client)
    raw = empfangeStr(client)
    return getKommPartner


def starteGui(client_socket,nick):
    global client, nickname
    client = client_socket
    nickname = nick
    app = tk.Tk()
    partner = get_Komm_Partner()
    app.title("Chatauswahl")
    app = gui(app,partner)
    app.mainloop()
