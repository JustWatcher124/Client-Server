import socket
import threading
import json

# alle Nutzer
NUTZER = []

# alle Nachrichten
NACHRICHTEN = []
##    [{"sender" : "...",
##      "empfaenger" : "...",
##      "nachricht" : "...",
##      "datum" : "..."
##        }]


def main():

    server = socket.socket()
    server.bind(("", 5000))
    server.listen(30)

    while True:
        client, client_adresse = server.accept()
        print("Verbindung mit", client_adresse, "aufgebaut)

        # Ausführen von client_server_kommunikation() im Hintergrund durch Multithreading
        # So können mehrere Verbindungen/Programmabschnitte gleichzeitig ausgeführt werden
        komm_thread = threading.Thread(target=client_server_kommunikation, args=(client,))
        komm_thread.start()
        

def client_server_kommunikation(client):
    benutzername = ""
    while True:
        # Nachricht vom Client empfangen und verarbeiten
        empfangen = empfangeStr(client)
        # An der ersten Stelle ist immer der Typ der Nachricht
        # Dadurch wird festgelegt, welche Daten geschickt oder angefordert werden
        nachrichtentyp = empfangen[0]
        empfangen = empfangen[1:]

        if nachrichtentyp == "1": # Client schickt Benutzernamen
            benutzername = empfangen
            print(benutzername, "ist nun angemeldet")
        elif nachrichtentyp == "3": # Client schickt Nachricht
            nachricht_speichern(benutzername, empfangen)
            print("Nachricht von", benutzername, "gespeichert")
        elif nachrichtentyp == "4": # Client fordert von ihm gesendete und an ihn gerichtete Nachrichten an
            nachrichten_an_client_schicken(client, benutzername)
            print("Nachrichten an", benutzername, "gesendet")
        else:
            print("ungueltiger Nachrichtentyp", nachrichtentyp, "von", benutzername)

def nachrichten_an_client_schicken(client, benutzername):
    # Nachrichten, die vom oder an den Client gesendet wurden
    nachrichten_mit_client = [n for n in NACHRICHTEN if n["sender"] == benutzername or n["empfaenger"] == benutzername]

    # in String umwandeln
    nachrichten_als_string = json.dumps(nachrichten_mit_client)
    
    sendeStr(client, nachrichten_als_string)
    sendeTrennByte(client)
    

def nachricht_speichern(benutzername_sender, empfangene_daten):
    pass



def empfangeStr(komm_s):
    weiter = True
    datenBytes = bytes()

    endByte = bytes([0])

    while weiter:
        chunk = komm_s.recv(1)
        if chunk == endByte or chunk == bytes([]):
            if len(datenBytes) > 0:
                weiter = False
            else:
                print("leere Nachricht empfangen!")
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

# Start
main()
