import tkinter as tk
import nachrichtFTjson
import socketLib

def chatGui(fenster):
    global window
    window = fenster
    toprow = tk.Frame(window,bg="#A9A9A9")
    tk.Button(toprow,text="Schließen",command= chatSchliessen).grid(row=0,column=0)
    tk.Button(toprow,text="refresh",command= refresh).grid(row=0,column=1)
    chatverlauf = tk.Frame(window, bg="#D3D3D3")
    bottomrow = tk.Frame(window, bg="#A9A9A9")
    text_input = tk.Text(bottomrow, height = 2, width=50).grid(row=2,column=0)
    tk.Button(bottomrow,text="Absenden", command= lambda: text_absenden(text_input))
    return window

def chatAuswahl(fenster):
    global window
    window = fenster
    window.title("Chatauswahl")



def chatSchliessen():
    global window
    window.destroy()

def text_absenden(text):
    global client
    nachricht = text.get(1.0,"end-1c")
    nickname = name
    print(nickname)
    window.destroy()


def refresh():
    global client, nickname
    socketLib.sendeStr(client,"4"+nickname)
    socketLib.sendeTrennByte(client)
    nachricht = socketLib.empfangeStr(client)
    print(stuff)


def starteChat(client_socket,nick):
    global client, nickname
    client = client_socket
    nickname = nick
    app = tk.Tk()
    app.title("Chatauswahl")
    app = chatGui(chat)
    app.mainloop()
