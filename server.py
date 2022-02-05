import socket
import threading
import json
from datetime import datetime

PORT = 5000

# alle Nutzer
NUTZER = []

# alle Nachrichten
NACHRICHTEN = []
##    [{"sender" : "...",
##      "empfaenger" : "...",
##      "nachricht" : "...",
##      "datum" : "hh:mm:ss,DD:MM:YYYY"
##        }]


def main():

    nachrichten_backup_einlesen()
    
    server = socket.socket()
    server.bind(("", PORT))
    server.listen(30)

    print("Server lauscht nun auf Port",PORT)

    while True:
        client, client_adresse = server.accept()
        print("Verbindung mit", client_adresse, "aufgebaut")

        # Ausführen von client_server_kommunikation() im Hintergrund durch Multithreading
        # So können mehrere Verbindungen/Programmabschnitte gleichzeitig und parallel ausgeführt werden
        komm_thread = threading.Thread(target=client_server_kommunikation, args=((client,client_adresse),))
        komm_thread.start()
        

def client_server_kommunikation(args):
    client, client_adresse = args
    benutzername = ""

    # Nachrichten vom Client empfangen und verarbeiten
    while True:
        empfangen = empfangeStr(client)
        # An der ersten Stelle ist immer der Typ der Nachricht festgelegt
        # Dadurch wird festgelegt, welche Daten geschickt oder angefordert werden
        nachrichtentyp = empfangen[0]
        empfangen = empfangen[1:]
        if nachrichtentyp == "0": # Client hat Verbindung getrennt 
            client.close()
            print(client_adresse, "hat die Verbindung getrennt")
            break
        elif nachrichtentyp == "1": # Client schickt Benutzernamen
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

    # Liste durch JSON-Modul in String umwandeln
    nachrichten_als_string = json.dumps(nachrichten_mit_client)

    # Nummer des Nachrichtentyps anfügen
    nachrichten_als_string = "5" + nachrichten_als_string
    
    sendeStr(client, nachrichten_als_string)
    sendeTrennByte(client)
    

def nachricht_speichern(sender, empfangene_daten):
    # Aufbau von empfangene_daten: "Empfänger Nachricht" -> Ab Leerzeichen nach Empfänger beginnt Nachricht

    # Aufteilen der Daten in Empfänger und Nachricht
    index_trennzeichen = empfangene_daten.index(" ")
    empfaenger = empfangene_daten[:index_trennzeichen]
    nachricht = empfangene_daten[index_trennzeichen+1:]

    # Aufbau Datum in der Nachricht : "hh:mm:ss,DD:MM:YYYY"
    jetzt = datetime.now()
    stunde = str(datetime.hour)
    minute = str(datetime.minute)
    sekunde = str(datetime.second)
    tag = str(datetime.day)
    monat = str(datetime.month)
    jahr = str(datetime.year)
    datum = "{hh}:{mm}:{ss},{DD}:{MM}:{YYYY}".format(hh=stunde, mm=minute, ss=sekunde, DD=tag, MM=monat, YYYY=jahr)

    # Nachricht mit Daten in die globale Liste anhängen
    NACHRICHTEN.append({
        "sender" : sender,
        "empfaenger" : empfaenger,
        "nachricht" : nachricht,
        "datum" : datum
        })

    # "Backup" der Nachrichten in externer Datei "nachrichten.log" speichern
    nachrichten_str = json.dumps(NACHRICHTEN) # Liste durch JSON-Modul in String umwandeln
    nachrichten_datei = open("nachrichten.log", "wt")
    nachrichten_datei.write(nachrichten_str)
    nachrichten_datei.close()
    
        

def nachrichten_backup_einlesen():
    # Versuchen Datei einzulesen
    try:
        datei = open("nachrichten.log", "rt")
        daten = datei.readlines()
        datei.close()
        
        if len(daten) > 0: # Falls Daten vorhanden
            NACHRICHTEN = json.loads(daten) # Daten durch JSON-Modul wieder in Liste und Dictionary umwandeln            
            print("gespeicherte Nachrichten erfolgreich eingelesen")
            
        else: # Falls Datei leer
            NACHRICHTEN = []
            print("keine gespeicherten Nachrichten gefunden")
            
    except FileNotFoundError: # Falls "nachrichten.log" noch nicht existiert
        NACHRICHTEN = []
        datei = open("nachrichten.log", "x")
        datei.close()
        print("keine gespeicherten Nachrichten gefunden")
        

def empfangeStr(komm_s):
    weiter = True
    datenBytes = bytes()

    endByte = bytes([0])

    while weiter:
        chunk = komm_s.recv(1)
        if chunk == endByte:
            print(chunk)
            if len(datenBytes) > 0: # Falls Daten empfangen wurden und TrennByte Ende der Nachricht signalisiert
                weiter = False
            else: # Falls leere Nachricht empfangen wurde
                print("leere Nachricht empfangen!")
                
        elif chunk == bytes([]): # wird empfangen, wenn Verbindung Client Verbindung getrennt hat
            return "0" # Nachrichtencode, dass Client Verbindung getrennt hat
                
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
if __name__ == "__main__":
    main()
