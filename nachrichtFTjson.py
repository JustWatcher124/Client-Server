from datetime import datetime
import json


def nachrichtFjson(string):
    s = json.loads(string)
    print(s)
