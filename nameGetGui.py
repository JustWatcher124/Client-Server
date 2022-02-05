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
    l = tk.Message(window,text="""Bitte geben Sie einen Benutzernamen ein.
    (Ohne Leerzeichen und Komma)""",width=100).grid()
    t = tk.Text(window,height = 1, width =45)
    e = tk.Label(window,text="")
    t.grid(row=1,column=0)
    tk.Button(window,text="Fertig",command= lambda: goodNick(t,e)).grid(row=1,column=1)
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
