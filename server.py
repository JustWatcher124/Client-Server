import socket
import threading

# alle Nutzer
NUTZER = []

# alle Nachrichten
NACHRICHTEN = []
##    [{"sender" : "...",
##      "empfaenger" : "...",
##      "nachricht" : "..."
##        }]


def main()

    verbindungs_s = socket.socket()
    verbindungs_s.bind(("", 5000))
    verbindungs_s.listen(30)

    while True:
        komm_s, client_adresse = verbindungs_s.accept()
        print("Verbindungsanfrage von", client_adresse)

        komm_thread = threading.Thread(target=client_server_kommunikation, args=(komm_s,))
        

def client_server_kommunikation(komm_s):

    komm_s.close()
        












        

def empfangeStr(komm_s):
    weiter = True
    datenBytes = bytes()

    endByte = bytes([0])

    while weiter:
        chunk = komm_s.recv(1)
        if chunk == endByte or chunk == bytes([]):
            weiter = False
        else:
            datenBytes = datenBytes + chunk

    datenStr = str(datenBytes, 'utf-8')

    return datenStr

def sendeStr(komm_s, datenStr):
    datenBytes = bytes(datenStr, 'utf-8')
    komm_s.sendall(datenBytes)

def sendeTrennByte(komm_s):
    trennByte = bytes([0])
    komm_s.sendall(trennByte)





















main()
