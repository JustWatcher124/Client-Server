import tkinter as tk
import nachrichtenFormatMaker
import socketLib

def chatGui(fenster):
    global window
    window = fenster
    tk.Button(window,text="Schließen",command= chatSchliessen).grid(row=0,column=0)
    tk.Button(window,text="refresh",command= refresh).grid(row=0,column=1)
    return window


def chatSchliessen():
    global window
    window.destroy()


def refresh():
    global client, nickname
    socketLib.sendeStr(client,"4"+nickname)
    socketLib.sendeTrennByte(client)
    stuff = socketLib.empfangeStr(client)
    print(stuff)


def starteChat(client_socket,nick):
    global client, nickname
    client = client_socket
    nickname = nick
    chat = tk.Tk()
    chat.title("Chatfenster")
    chat = chatGui(chat)
    chat.mainloop()
