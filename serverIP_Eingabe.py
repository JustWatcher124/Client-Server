import tkinter


def eingabe_lesen(ip,er_ip,port,er_port):
    global serverip
    inp = ip.get(1.0,"end-1c")
    p = port.get(1.0,"end-1c")
    if is_it_ip_format(inp) and is_it_port(p):
        print("Die eingegebene Server-IP ist: ",inp +":"+ p)
        serverip = inp +":"+  p
        fenster.destroy()
    else:
        er_ip.config(text="Ihr Eingabe war nicht im IPv4 Format (X.X.X.X)")


def is_it_port(port):
    try:
        int(port)
    except:
        return False
    return True


def serverIP():
    tkinter.Label(fenster,text = "Bitte geben Sie die IPv4 des Nachrichten Servers an").grid(row=0)

    eingabe_IP = tkinter.Text(fenster,height=1)
    error_IP = tkinter.Label(fenster,text="")

    fertig_button = tkinter.Button(fenster,text="Fertig",
    command= lambda: eingabe_lesen(eingabe_IP,error_IP,eingabe_Port,error_PORT))


    eingabe_Port = tkinter.Text(fenster,height=1)
    error_PORT = tkinter.Label(fenster,text="")

    abbrechen = tkinter.Button(fenster,text="Abbrechen",command=abbruch)


    eingabe_IP.grid(row=1,column=0)
    error_IP.grid(row=2)
    tkinter.Label(fenster,text = "Bitte geben Sie den Port an").grid(row=3)
    eingabe_Port.grid(row=4,column=0)
    error_PORT.grid(row=5)
    fertig_button.grid(row=6,column=1)
    abbrechen.grid()
    fenster.mainloop()


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
    global serverip
    serverip = "A"
    fenster.destroy()


def getIP():
    serverIP()
    while serverip=="":
        pass
    return serverip

serverip = ""
fenster = tkinter.Tk()
fenster.title("Eingabe der IP+Port des Chat-Servers")
