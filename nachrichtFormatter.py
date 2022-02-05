from datetime import datetime
import json


def nachrichtFjson(string):
    s = json.loads(string)
    komm_partner = s.keys()
    print(komm_partner)
    print(type(s))

def getKommPartner(string):
    return json.loads(string).keys()


def nachrichtTjson(sender,empfaenger,nachricht):
    x = {"sender":sender,"empfaenger":empfaenger,"nachricht":nachricht}
    return str(x)

def verlaufToJson(verlaufs_string):
    s = ""
    res = verlaufs_string.strip('][').split('}, ')
    messages = []
    for quickfix in res:
        if "}" not in quickfix:
            messages.append(quickfix+"}")
        else:
            messages.append(quickfix)
    for mes in messages:
        print(mes)
        message = json.loads(mes)
        s+=message["sender"]+"\n"
    return s
