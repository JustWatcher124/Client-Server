
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
    datenStr = datenBytes.decode('utf-8').replace("'",'"')
    return datenStr


def sendeStr(komm_s, datenStr):
    datenBytes = bytes(datenStr, 'utf-8')
    komm_s.sendall(datenBytes)


def sendeTrennByte(komm_s):
    trennByte = bytes([0])
    komm_s.sendall(trennByte)
