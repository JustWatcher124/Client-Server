import serverIP_Eingabe
import chatGUI
import socketLib
import socket
import tkinter
import time
print('''Willkommen bei unserem super-tollem-Nachrichtensystem,
bevor es losgehen kann, brauchen Wir die IP des Servers an.
(Es sollte sich ein neues Fenster geöffnet haben)''')

def startGui():
    chatGUI()

client = socket.socket()
client.settimeout(10)
ip, port = serverIP_Eingabe.getIP().split(":")
try:
    client.connect((ip,int(port)))
except TimeoutError:
    print("Die Verbindung ist abgebrochen (TimeOut)")
except:
    print("Etwas unvorhergesehenes ist passiert")
else:
    startGui()

print("Sie sind erflogreich mit dem Server verbunden")
print(ip,port)
