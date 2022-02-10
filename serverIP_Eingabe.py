import tkinter as tk
serverip = ""
# Eingabefenster für die IP und den Port des Servers


# Funktion zum Überprüfen ob die eingaben gut sind
def eingabe_lesen(ip,er_ip,port,er_port):
    global serverip
    global window
    inp = ip.get(1.0,"end-1c")
    p = port.get(1.0,"end-1c")
    if is_it_ip_format(inp) and is_it_port(p):
        print("Die eingegebene Server-IP ist: ",inp +":"+ p)
        serverip = inp +":"+  p
        window.destroy()
    if not is_it_ip_format(inp):
        er_ip.config(text="Ihr Eingabe war nicht im IPv4 Format (X.X.X.X)")
    if not is_it_port(p):
        er_port.config(text="Das ist kein gültiger Port")

# Funktion die überprüft ob aus dem eingegebenen String port ein int
# gemacht werden kann (Das ist unser Kriterium für Ports)
def is_it_port(port):
    try:
        int(port)
    except:
        return False
    return True

# Funktion zum Befüllen des Fensters
def serverIPGui(fenster):
    global window
    window = fenster
    tk.Label(window,text = "Bitte geben Sie die IPv4 des Nachrichten Servers an").grid(row=0)

    eingabe_IP = tk.Text(window,height=1,width=50)
    error_IP = tk.Label(window,text="")

    eingabe_Port = tk.Text(window,height=1,width=50)
    error_PORT = tk.Label(window,text="")

    eingabe_IP.grid(row=1,column=0)
    error_IP.grid(row=2)
    tk.Label(window,text = "Bitte geben Sie den Port an").grid(row=3)
    eingabe_Port.grid(row=4,column=0)
    error_PORT.grid(row=5)
    tk.Button(window,text="Fertig",
    command= lambda: eingabe_lesen(eingabe_IP,error_IP,eingabe_Port,error_PORT)
    ).grid(row=4,column=1)
    tk.Button(window,text="Abbrechen",command=abbruch)
    tk.Button(window,text="Standard", command=standard).grid()
    return window


# Funktion zum Überprüfen ob der eingegebene String ip
# im Format "X.X.X.X" wo X ein int von 0 - 999 ist
def is_it_ip_format(ip):
    ip = ip.split(".")
    try:
        for i in ip:
            int(i)
            if 0< len(i) <4:
                pass
            else:
                raise Exception()
    except:
        return False
    return True


def abbruch():
    global serverip, window
    serverip = "A"
    window.destroy()

# Standart-IP und Port des Servers ist 127.0.0.1:5000
# Auch hier zur Vereinfachung des Testens
def standard():
    global serverip, window
    serverip = "127.0.0.1:5000"
    window.destroy()

# Start-Funktion die das Fenster kontrolliert
# Gibt die eingebene Server IP zurück als String ("127.0.0.1:5000")
def getIP():
    global serverip
    chat = tk.Tk()
    chat.title("Chat")
    chat = serverIPGui(chat)
    chat.mainloop()
    return serverip
