import tkinter as tk
import nachrichtFTjson
import socketLib

def chatGui(fenster):
    global window
    window = fenster
    toprow = tk.Frame(window,bg="#A9A9A9", height=50)
    chatverlauf = tk.Frame(window, bg="#D3D3D3")
    verlauf = tk.Label(chatverlauf,text="Es sind keine Nachrichten vorhanden, drücke auf 'refresh'",width=50)
    tk.Button(toprow,text="Schließen",command= chatSchliessen).grid(row=0,column=0)
    tk.Button(toprow,text="refresh",command= lambda: refresh(verlauf)).grid(row=0,column=2)
    bottomrow = tk.Frame(window, bg="#A9A9A9")
    text_input = tk.Text(bottomrow, height = 2, width=50).grid(row=2,column=0)
    tk.Button(bottomrow,text="Absenden", command= lambda: text_absenden(text_input))
    toprow.pack()
    verlauf.pack()
    chatverlauf.pack()
    bottomrow.pack()
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


def refresh(chat_verlauf):
    global client, nickname
    socketLib.sendeStr(client,"4"+nickname)
    socketLib.sendeTrennByte(client)
    nachricht_raw = socketLib.empfangeStr(client)
    nachricht = nachrichtFTjson.nachrichtFjson(nachricht_raw)
    

def starteChat(client_socket,nick):
    global client, nickname
    client = client_socket
    nickname = nick
    app = tk.Tk()
    app.title("Chatauswahl")
    app = chatGui(app)
    app.mainloop()
