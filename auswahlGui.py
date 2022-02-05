import tkinter as tk
from nachrichtFormatter import *
from socketLib import *
import chatGui
chat_partner = ""

def gui(fenster,names):
    global window
    window = fenster
    toprow = tk.Frame(window,bg="#A9A9A9")
    bottomrow = tk.Frame(window)
    partners = tk.Frame(window)
    partners = refresh(partners,names)
    tk.Button(toprow,text="Schließen",command= guiSchliessen).grid(row=0,column=0)
    tk.Button(toprow,text="refresh",command= lambda: refresh(partners,get_Komm_Partner())).grid(row=0,column=2)
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


def chat_beginnen(nc,er_nc):
    global window, chat_partner
    name = nc.get(1.0,"end-1c")
    if " " in name or "," in name:
        er_nc.config(text="Unzulässiger Name")
    else:
        chat_partner = name
        print("Neuer Chat mit:",chat_partner)
        window.destroy()


def get_Komm_Partner():
    global client
    sendeStr(client,"2"); sendeTrennByte(client)
    raw = empfangeStr(client)
    print(raw,"Raw empfangen beim Anfragen auf Chatverläufe")
    return getKommPartner(raw[1:])


def clear_widgets(tk_frame):
    for widget in tk_frame.winfo_children():
        widget.destroy()


def refresh(partners,names):
    clear_widgets(partners)
    if len(names)>0:
        for partner in names:
            tk.Button(partners,text=partner, command= lambda: chat_Aufruf(partner)).pack()
    else:
        tk.Label(partners,text="Sie haben keine Chatverläufe!").pack()
    return partners


def guiSchliessen():
    global window
    window.destroy()


def chat_Aufruf(name):
    global window, chat_partner
    chat_partner = name
    print("Chat mit",chat_partner," aufgerufen")
    window.destroy()


def starteGui(client_socket,nick):
    global client, nickname, chat_partner
    client = client_socket
    nickname = nick
    app = tk.Tk()
    partner = get_Komm_Partner()
    app.title("Chatauswahl")
    app = gui(app,partner)
    app.mainloop()
    chatGui.starteGui(client,nickname,chat_partner)
