import serverIP_Eingabe
import nameGetGui
import socketLib
import socket
import chatGui
import auswahlGui
# Hauptprogramm für den Client
# Beinhaltet client, nickname und serverip

print('''Willkommen bei unserem super-tollem-Nachrichtensystem,
bevor es losgehen kann, brauchen Wir die IP des Servers an.
(Es sollte sich ein neues Fenster geöffnet haben)''')

# Client wird als socket.socket instanziiert
client = socket.socket()
client.settimeout(10) # Sockettimeout = Zeit bis der Client nach Verbindungsabbruch einen Fehler bringt
try:
    nickname = nameGetGui.main()
    if nickname == "":
        raise NickNameError()
    ip,port = serverIP_Eingabe.getIP().split(":")
except NickNameError:
    print("Sie haben das Fenster Geschlossen")
except:
    print("Sie haben Abbrechen gedrückt")
print("Sie sind als",nickname,"angemeldet")
print(ip,port)
try:
    client.connect((ip,int(port)))
    socketLib.sendeStr(client,"1"+nickname)
    socketLib.sendeTrennByte(client)
except TimeoutError:
    print("Die Verbindung ist abgebrochen (TimeOut)")
except:
    print("Etwas unvorhergesehenes ist passiert")
else:
    print("Alles Gut")
    auswahlGui.starteGui(client,nickname)
# Client schickt eine 0 an Server um Trennen der Verbindung zu signalisieren
socketLib.sendeStr(client,"0");socketLib.sendeTrennByte(client)
client.close()
print("Schönen Tag noch")

