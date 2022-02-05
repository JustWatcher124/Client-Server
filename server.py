import socket
import threading
import json
from datetime import datetime

# Client-Server-Protokoll
# Aufbau des empfangenen Strings bei Kommunikation immer:
#  1. Zeichen: Nachrichtencode
#  ab 2. Zeichen: Nutzdaten

# Nachrichtencodes (zum identifizieren, welche Art von Daten empfangen wurden)
# 1-> Client schickt Benutzername an Server -> 1Name
# 2-> Client frägt Chatübersicht an -> 2
# 3-> Server schickt Client Chatüberischt -> 3{"Name": Anzahl ungelesenen Nachrichten,}
# 4-> Client frägt Chat an -> 4Kommunikationspartner
# 5-> Server schickt alle Nachrichten von und an Benutzer an dessen Client ->5[Liste der Nachrichten]
# 6-> Benutzer hat neue Nachricht (ohne Datum) gesendet, Server speichert nun die Nachricht ->6{Nachricht}

# Aufbau einer Nachricht:
#   {"sender": "...",
#    "empfaenger": "...",
#    "datum": "hh:mm:ss,DD:MM:YYYY",
#    "nachricht": "..."}
#    }

PORT = 5000

# alle Nutzer
NUTZER = []

# alle Nachrichten
NACHRICHTEN = {}
##    {"benutzername1":{
##          "kommunikationspartner1":[
##              {"sender": "...",
##               "empfaenger": "...",
##               "datum": "hh:mm:ss,DD:MM:YYYY",
##               "nachricht": "..."}
##              }
##          ]
##      }

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
    global NACHRICHTEN

    client, client_adresse = args
    benutzername = ""
    try: 
        # Nachrichten vom Client empfangen und verarbeiten
        while True:
            empfangen = empfangeStr(client)
            print("log", client_adresse, empfangen)
            # An der ersten Stelle ist immer der Typ der Nachricht festgelegt
            # Dadurch wird festgelegt, welche Daten geschickt oder angefordert werden
            nachrichtentyp = empfangen[0]
            empfangen = empfangen[1:]
            if nachrichtentyp == "0": # Client hat Verbindung getrennt 
                client.close()
                raise ConnectionResetError # springt in except Teil
            elif nachrichtentyp == "1": # Client schickt Benutzernamen
                benutzername = empfangen
                if benutzername not in NACHRICHTEN.keys():
                    benutzer_registrieren(benutzername)
                print(client_adresse, "ist nun als", benutzername, "angemeldet")
            elif nachrichtentyp == "2": # Client frägt Chatübersicht an
                pass
            elif nachrichtentyp == "4": # Client fordert von ihm gesendete und an ihn gerichtete Nachrichten an
                nachrichten_an_client_schicken(client, benutzername)
                print("Nachrichten an", benutzername, "gesendet")
            elif nachrichtentyp == "6": # Client schickt Nachricht
                nachricht_speichern(benutzername, empfangen)
                print("Nachricht von", benutzername, client_adresse, "gespeichert")
            else:
                print("ungueltiger Nachrichtentyp", nachrichtentyp, "von", benutzername, client_adresse)
                
    except ConnectionResetError:
        print(benutzername, client_adresse, "hat die Verbindung getrennt")
        return # beendet diese Funktion und diesen Thread

def benutzer_registrieren(neuer_nutzer):
    global NACHRICHTEN
    # benutzername als neuen Kommunikationspartner bei allen aneren Nutzern hinzufügen
    for nutzer in NACHRICHTEN.keys():
        NACHRICHTEN[nutzer][neuer_nutzer] = []

    # benutzername als neuen Nutzer zu Nachrichten hinzufügen
    alle_anderen_nutzer = NACHRICHTEN.keys()
    NACHRICHTEN[neuer_nutzer] = {n:[] for n in alle_anderen_nutzer}


    # Änderungen in nachrichten.json speichern
    nachrichten_str = json.dumps(NACHRICHTEN)
    nachrichten_datei = open("nachrichten.json", "wt")
    nachrichten_datei.write(nachrichten_str)
    nachrichten_datei.close()


def nachrichten_an_client_schicken(client, benutzername):
    global NACHRICHTEN

    # alle Chats des benutzers
    nachrichten_mit_client = NACHRICHTEN[benutzername]

    # Dictionary durch JSON-Modul in String umwandeln
    nachrichten_als_string = json.dumps(nachrichten_mit_client)

    # Nummer des Nachrichtentyps anfügen
    nachrichten_als_string = "5" + nachrichten_als_string
    
    sendeStr(client, nachrichten_als_string)
    sendeTrennByte(client)
    

def nachricht_speichern(sender, empfangene_daten):
    global NACHRICHTEN

    # Aufbau von empfangene_daten: {"sender": "...",
    #                  "empfaenger": "...",
    #                  "nachricht": "..."}
    #                 }

    nachricht = json.loads(empfangene_daten)

    # Datum muss noch hinzugefügt werden
    # Aufbau Datum in der Nachricht : "hh:mm:ss,DD:MM:YYYY"
    jetzt = datetime.now()
    stunde = str(datetime.hour)
    minute = str(datetime.minute)
    sekunde = str(datetime.second)
    tag = str(datetime.day)
    monat = str(datetime.month)
    jahr = str(datetime.year)
    datum = "{hh}:{mm}:{ss},{DD}:{MM}:{YYYY}".format(hh=stunde, mm=minute, ss=sekunde, DD=tag, MM=monat, YYYY=jahr)

    # Datum in Nachricht speichern
    nachricht["datum"] = datum
    # Lesestatus in Nachricht speichern
    nachricht["gelesen"] = False

    # Empfänger und Sender aus Nachricht auslesen
    empfaenger = nachricht["empfaenger"]
    sender = nachricht["sender"]

    # Nachricht bei Sender und Empfänger speichern
    NACHRICHTEN[empfaenger][sender].append(nachricht)
    NACHRICHTEN[sender][empfaenger].append(nachricht)

    # "Backup" der Nachrichten in externer Datei "nachrichten.json" speichern
    nachrichten_str = json.dumps(NACHRICHTEN) # Liste durch JSON-Modul in String umwandeln
    nachrichten_datei = open("nachrichten.json", "wt")
    nachrichten_datei.write(nachrichten_str)
    nachrichten_datei.close()
    
        

def nachrichten_backup_einlesen():
    global NACHRICHTEN

    # Versuchen Datei einzulesen
    try:
        datei = open("nachrichten.json", "rt")
        daten = datei.read()
        datei.close()
        
        if len(daten) > 0: # Falls Daten vorhanden
            NACHRICHTEN = json.loads(daten) # Daten durch JSON-Modul wieder in Liste und Dictionary umwandeln            
            print("gespeicherte Nachrichten erfolgreich eingelesen")
            print(NACHRICHTEN)
            
        else: # Falls Datei leer
            NACHRICHTEN = {}
            print("keine gespeicherten Nachrichten gefunden")
            
    except FileNotFoundError: # Falls "nachrichten.json" noch nicht existiert
        NACHRICHTEN = {}
        datei = open("nachrichten.json", "x")
        datei.close()
        print("keine gespeicherten Nachrichten gefunden")
        

def empfangeStr(komm_s):
    weiter = True
    datenBytes = bytes()

    endByte = bytes([0])

    while weiter:
        chunk = komm_s.recv(1)
        if chunk == endByte:
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
