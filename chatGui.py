import tkinter as tk
from nachrichtFTjson import *
import socketLib

def gui(fenster):
    global window
    window = fenster
    toprow = tk.Frame(window,bg="#A9A9A9", height=50)
    chatverlauf = tk.Frame(window, bg="#D3D3D3",height=250)
    verlauf = tk.Label(chatverlauf,text="Es sind keine Nachrichten vorhanden, drücke auf 'refresh'",width=50)
    tk.Button(toprow,text="Schließen",command= chatSchliessen).grid(row=0,column=0)
    tk.Button(toprow,text="refresh",command= lambda: refresh(verlauf)).grid(row=0,column=2)
    bottomrow = tk.Frame(window, bg="#A9A9A9")
    text_input = tk.Text(bottomrow, height = 2, width=50).grid(row=2,column=0)
    tk.Button(bottomrow,text="Absenden", command= lambda: text_absenden(text_input)).grid(row=2,column=1)
    toprow.pack(side="top")
    verlauf.pack()
    chatverlauf.pack()
    bottomrow.pack(side="bottom")
    return window



def chatSchliessen():
    global window
    window.destroy()

def text_absenden(text):
    global client
    nachricht = text.get(1.0,"end-1c")
    print(nachricht)


def refresh(chat_verlauf):
    global client, nickname
    socketLib.sendeStr(client,"4"+nickname)
    socketLib.sendeTrennByte(client)
    nachricht_raw = socketLib.empfangeStr(client)
    nachricht = nachrichtFTjson.nachrichtFjson(nachricht_raw[1:])

def starteGui(client_socket,nick):
    global client, nickname
    client = client_socket
    nickname = nick
    app = tk.Tk()
    app.title("stuff")
    app = gui(app)
    app.mainloop()
