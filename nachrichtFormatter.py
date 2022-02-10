from datetime import datetime
import json
# Funktionsbibliothek für die Verarbeitung der vom Server geschickten Daten


# Funktion um die vom Server geschickte Chatübersicht zu verarbeiten
# gibt eine Liste mit partnername "ANZ.Ungelesener Nachrichten" zurück
def getKommPartner(string):
    partners = []
    d = json.loads(string)
    for i in d.keys():
        partners.append(str(i)+" "+"("+str(d[i])+")")
    return partners

# Funktion zum Senden von Chatnachrichten an den Server
# Gibt einen String zurück, der in sich ein json ist (siehe x = {...})
def nachrichtTjson(sender,empfaenger,nachricht):
    x = {"sender":sender,"empfaenger":empfaenger,"nachricht":nachricht}
    return str(x)

# Funktion um den vom Server geschickten Chatverlauf zu verstehen
# gibt Liste zurück wo jede Nachricht 1 json Element ist
# wenn kein Chatverlauf existiert return ""
def verlaufToJson(verlaufs_string):
    res = verlaufs_string.strip('][').split('}, ')
    messages = []
    print(res)
    if res != ['']:
        for quickfix in res:
            if "}" not in quickfix:
                messages.append(json.loads(quickfix+"}"))
            else:
                messages.append(json.loads(quickfix))
        return messages
    else:
        return ''

