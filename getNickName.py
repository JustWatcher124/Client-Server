import tkinter as tk
nickname = ""



def getNick(n):
    global getNN
    getNN = n
    getNN.title("Eingabe ihres Benutzernamens")
    initNickFenster()
    while nickname=="":
        pass
    return nickname


def initNickFenster():
    window = tk.Frame()
    l = tk.Message(window,text="""Bitte geben Sie einen Benutzernamen ein.
    (Ohne Leerzeichen und Komma)""",width=100).grid()
    t = tk.Text(window,height = 1, width =45)
    e = tk.Label(window,text="")
    t.grid(row=1,column=0)
    tk.Button(text="Fertig",command= lambda: goodNick(t,e)).grid(row=1,column=1)
    e.grid(row=2)
    tk.Button(window,text="Abbrechen",command=abbruch).grid()
    getNN.mainloop()

def abbruch():
    global nickname
    nickname = " "
    window.destroy()


def goodNick(text,error):
    global nickname
    name = text.get(1.0,"end-1c")
    if " " in name or "," in name:
        error.config(text="Unzulässiger Name")
    else:
        nickname = name
        print(nickname)
        window.destroy()
