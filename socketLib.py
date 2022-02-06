
def empfangeStr(komm_s):
    weiter = True
    datenBytes = bytes()
    endByte = bytes([0])
    while weiter:
        chunk = komm_s.recv(1)
        if chunk == endByte:
            if len(datenBytes) > 0:  # Falls Daten empfangen wurden und TrennByte Ende der Nachricht signalisiert
                weiter = False
            else:  # Falls leere Nachricht empfangen wurde
                print("leere Nachricht empfangen!")

        elif chunk == bytes([]):  # wird empfangen, wenn Verbindung Client Verbindung getrennt hat
            return "0"  # Nachrichtencode, dass Client Verbindung getrennt hat

        else:
            datenBytes = datenBytes + chunk

    datenStr = datenBytes.decode('utf-8').replace("'",'"')
    return datenStr


def sendeStr(komm_s, datenStr):
    datenBytes = bytes(datenStr, 'utf-8')
    komm_s.sendall(datenBytes)


def sendeTrennByte(komm_s):
    trennByte = bytes([0])
    komm_s.sendall(trennByte)
