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
    x = json.loads( str({"sender":sender,"empfaenger":empfaenger,"nachricht":nachricht}))
    return json.dumps(x)
