import socket
import threading
import json
from socketLib import *
from datetime import datetime
import time

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

    # Thread um regelmäßig backups in "nachrichten.json" zu speichern
    backup_thread = threading.Thread(target=mache_backups)
    backup_thread.start()

    print("Server lauscht nun auf Port",PORT,"\n")

    while True:
        client, client_adresse = server.accept()
        print("Verbindung mit", client_adresse, "aufgebaut\n")

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
                print(client_adresse, "ist nun als", benutzername, "angemeldet\n")
            elif nachrichtentyp == "2": # Client frägt Chatübersicht an
                chatuebersicht_schicken(client, benutzername)
                print("Chatüberischt wurde an", benutzername, client_adresse, "geschickt\n")
            elif nachrichtentyp == "4": # Client fordert Chatverlauf mit Kommunikationspartner an
                kommunikationspartner = empfangen
                chat_an_client_schicken(client, benutzername, kommunikationspartner)
                print("Chatverlauf mit", kommunikationspartner,"an", benutzername, client_adresse, "gesendet\n")
            elif nachrichtentyp == "6": # Client schickt Nachricht
                nachricht_speichern(benutzername, empfangen)
                print("Nachricht von", benutzername, client_adresse, "gespeichert\n")
            else:
                print("ungueltiger Nachrichtentyp", nachrichtentyp, "von", benutzername, client_adresse,"\n")

    except ConnectionResetError:
        print(benutzername, client_adresse, "hat die Verbindung getrennt\n")
        return # beendet diese Funktion und diesen Thread

def chatuebersicht_schicken(client, benutzername):
    chats = NACHRICHTEN[benutzername]

    # Chatübersicht generieren
    chatuebersicht = {} # {"Name": Anzahl ungelesenen Nachrichten,}
    for n in chats.keys():
        ungelesene_nachrichten = berechne_ungelesene_nachrichten(benutzername, chats[n])
        chatuebersicht[n] = ungelesene_nachrichten

    # Dictionary durch JSON-Modul in String umwandeln
    chatuebersicht_als_string = json.dumps(chatuebersicht)

    # Nummer des Nachrichtentyps anfügen
    chatuebersicht_als_string = "3" + chatuebersicht_als_string

    sendeStr(client, chatuebersicht_als_string)
    sendeTrennByte(client)



def berechne_ungelesene_nachrichten(anfragesteller, chatListe):
    ungelesene_nachrichten = 0
    for i in range(len(chatListe)-1,-1,-1): # durchläuft Indices der Liste rückwärts
        if chatListe[i]["empfaenger"] == anfragesteller and not chatListe[i]["gelesen"]:
            ungelesene_nachrichten += 1
        else:
            break
    return ungelesene_nachrichten


def benutzer_registrieren(neuer_nutzer):
    global NACHRICHTEN
    # benutzername als neuen Kommunikationspartner bei allen aneren Nutzern hinzufügen
    for nutzer in NACHRICHTEN.keys():
        NACHRICHTEN[nutzer][neuer_nutzer] = []

    # benutzername als neuen Nutzer zu Nachrichten hinzufügen
    alle_anderen_nutzer = NACHRICHTEN.keys()
    NACHRICHTEN[neuer_nutzer] = {n:[] for n in alle_anderen_nutzer}


def chat_an_client_schicken(client, benutzername, kommunikationspartner):
    global NACHRICHTEN

    # alle Nachrichten des Benutzers mit dem Kommunikationspartner
    chat = NACHRICHTEN[benutzername][kommunikationspartner]

    # Dictionary durch JSON-Modul in String umwandeln
    chat_als_string = json.dumps(chat)

    # Nummer des Nachrichtentyps anfügen
    chat_als_string = "5" + chat_als_string

    sendeStr(client, chat_als_string)
    sendeTrennByte(client)

    # Falls letzte Nachricht an Benutzer gerichtet war und dieser die Nachricht abgefragt hat
    if not chat[len(chat)-1]["gelesen"] and chat[len(chat)-1]["empfaenger"] == benutzername:
        # alle Nachrichten auf gelesen setzen
        for nachricht in chat:
            nachricht["gelesen"] = True

def nachricht_speichern(sender, empfangene_daten):
    global NACHRICHTEN


    # Aufbau von empfangene_daten: {"sender": "...",
    #                  "empfaenger": "...",
    #                  "nachricht": "..."}
    #                 }

    nachricht = json.loads(empfangene_daten)

    # falls Empfänger noch nicht im registriert ist
    empfaenger = nachricht["empfaenger"]
    if empfaenger not in NACHRICHTEN.keys():
        benutzer_registrieren(empfaenger)

    # Datum muss noch hinzugefügt werden
    # Aufbau Datum in der Nachricht : "hh:mm:ss,DD:MM:YYYY"
    jetzt = datetime.now()
    stunde = str(jetzt.hour)
    minute = str(jetzt.minute)
    sekunde = str(jetzt.second)
    tag = str(jetzt.day)
    monat = str(jetzt.month)
    jahr = str(jetzt.year)
    datum = "{hh}:{mm}:{ss},{DD}.{MM}.{YYYY}".format(hh=stunde, mm=minute, ss=sekunde, DD=tag, MM=monat, YYYY=jahr)

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



def nachrichten_backup_einlesen():
    global NACHRICHTEN

    # Versuchen Datei einzulesen
    try:
        datei = open("nachrichten.json", "rt")
        daten = datei.read()
        datei.close()

        if len(daten) > 0: # Falls Daten vorhanden
            NACHRICHTEN = json.loads(daten) # Daten durch JSON-Modul wieder in Liste und Dictionary umwandeln
            print("Backup erfolgreich eingelesen")

        else: # Falls Datei leer
            NACHRICHTEN = {}
            print("kein Backup gefunden")

    except FileNotFoundError: # Falls "nachrichten.json" noch nicht existiert
        NACHRICHTEN = {}
        datei = open("nachrichten.json", "x")
        datei.close()
        print("kein Backup gefunden")

def mache_backups():
    global NACHRICHTEN

    # Wiederholt sich alle 30 Sekunden
    while True:
        time.sleep(30)

        # Backup der Nachrichten in externer Datei "nachrichten.json" speichern
        nachrichten_str = json.dumps(NACHRICHTEN, indent=4)  # Liste durch JSON-Modul in String umwandeln

        nachrichten_datei = open("nachrichten.json", "wt")
        nachrichten_datei.write(nachrichten_str)
        nachrichten_datei.close()

        print("Backup gespeichert\n")

# Start
if __name__ == "__main__":
    main()
