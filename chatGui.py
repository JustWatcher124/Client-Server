import tkinter as tk
from tkinter import ttk
from nachrichtFormatter import *
from socketLib import *

def gui(fenster):
    global window
    window = fenster
    toprow = tk.Frame(window, height=50)
    chatverlauf = tk.Canvas(window, bg="#D3D3D3",height=250)
    kein_verlauf = tk.Label(toprow,text="Es sind keine Nachrichten vorhanden, drücke auf 'refresh'",width=50)
    tk.Button(toprow,text="Schließen",command= chatSchliessen).grid(row=0,column=0)
    tk.Button(toprow,text="refresh",command= lambda: refresh(kein_verlauf,chatverlauf)).grid(row=0,column=2)
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


def chatSchliessen():
    global window
    window.destroy()

def text_absenden(text,k_v,cv):
    global client, neuer_chat
    nachricht = text.get(1.0,"end-1c")
    nachricht_zum_server(nachricht)
    neuer_chat = False
    refresh(k_v,cv)

def nachricht_zum_server(nachricht):
    global nickname, komm_partner
    raw = nachrichtTjson(nickname,komm_partner,nachricht)
    sendeStr(client,"6"+raw); sendeTrennByte(client)


def clear_widgets(tk_frame):
    for widget in tk_frame.winfo_children():
        widget.destroy()


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

