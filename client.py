import serverIP_Eingabe
import nameGetGui
import socketLib
import socket
import chatGui
print('''Willkommen bei unserem super-tollem-Nachrichtensystem,
bevor es losgehen kann, brauchen Wir die IP des Servers an.
(Es sollte sich ein neues Fenster geöffnet haben)''')


client = socket.socket()
client.settimeout(10)
try:
    nickname = nameGetGui.main()
    ip,port = serverIP_Eingabe.getIP().split(":")
except ValueError:
    print("Sie haben Abbrechen gedrückt")
print(nickname, "Im client")
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


chatGui.starteChat(client,nickname)
