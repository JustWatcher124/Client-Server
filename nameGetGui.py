import tkinter as tk
nickname = ""


def main():
    global nickname
    chat = tk.Tk()
    chat.title("Chat")
    chat = initNickFenster(chat)
    chat.mainloop()
    return nickname

def initNickFenster(gui):
    global window
    window = gui
    l = tk.Label(window,text="""Bitte geben Sie einen Benutzernamen ein.\n
    (Ohne Leerzeichen und Komma)""").grid()
    nick_in = tk.Text(window,height = 1, width =45)
    e = tk.Label(window,text="")
    nick_in.grid(row=1,column=0)
    tk.Button(window,text="Fertig",command= lambda: goodNick(nick_in,e)).grid(row=1,column=1)
    e.grid(row=2)
    tk.Button(window,text="Abbrechen",command=abbruch).grid()
    tk.Button(window,text="Standard", command=standard).grid()
    window.grid()
    return gui


def abbruch():
    global window
    window.destroy()

def standard():
    global nickname, window
    nickname = "JustWatcher124"
    window.destroy()

def goodNick(text,error):
    global nickname, window
    name = text.get(1.0,"end-1c")
    if " " in name or "," in name:
        error.config(text="Unzulässiger Name")
    else:
        nickname = name
        print(nickname)
        window.destroy()
