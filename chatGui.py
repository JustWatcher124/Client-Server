import tkinter as tk
from nachrichtFormatter import *
from socketLib import *

def gui(fenster):
    global window
    window = fenster
    toprow = tk.Frame(window,bg="#A9A9A9", height=50)
    chatverlauf = tk.Frame(window, bg="#D3D3D3",height=250)
    kein_verlauf = tk.Label(chatverlauf,text="Es sind keine Nachrichten vorhanden, drücke auf 'refresh'",width=50)
    verlauf = tk.Label(chatverlauf,text="")
    tk.Button(toprow,text="Schließen",command= chatSchliessen).grid(row=0,column=0)
    tk.Button(toprow,text="refresh",command= lambda: refresh(kein_verlauf,verlauf)).grid(row=0,column=2)
    bottomrow = tk.Frame(window, bg="#A9A9A9")
    text_input = tk.Text(bottomrow, height = 2, width=50)
    tk.Button(bottomrow,text="Absenden", command= lambda: text_absenden(text_input,kein_verlauf,verlauf)).grid(row=2,column=1)
    text_input.grid(row=2,column=0)
    toprow.pack(side="top")
    verlauf.pack()
    kein_verlauf.pack()
    chatverlauf.pack()
    bottomrow.pack(side="bottom")
    #refresh(verlauf,verlauf)
    return window


def chatSchliessen():
    global window
    window.destroy()

def text_absenden(text,k_v,cv):
    global client
    nachricht = text.get(1.0,"end-1c")
    nachricht_zum_server(nachricht)
    refresh(k_v,cv)

def nachricht_zum_server(nachricht):
    global nickname, komm_partner
    raw = nachrichtTjson(nickname,komm_partner,nachricht)
    sendeStr(client,"6"+raw); sendeTrennByte(client)


def refresh(kein_verlauf,chat_verlauf):
    global client, komm_partner
    sendeStr(client,"4"+komm_partner)
    sendeTrennByte(client)
    nachricht_raw = empfangeStr(client)
    #print(nachricht_raw, "Empfangene Nachricht")
    nachricht = verlaufToJson(nachricht_raw[1:])
    kein_verlauf.destroy()
    chat_verlauf.config(text=nachricht)

def starteGui(client_socket,nick,partner):
    global client, nickname, komm_partner
    client = client_socket
    nickname = nick
    komm_partner = partner
    app = tk.Tk()
    app.title("Ihr Chat mit:"+komm_partner)
    app = gui(app)
    app.mainloop()
