# Client-Server
A school project that will inevitably steal our sleep and/or sanity

Ein Python-Programm mit dem man zwischen einem Server und (bis zu) 20 Clients gleichzeitig Nachrichten schreiben kann.
Funktioniert dank der Python socket Bibliothek

Um es zu starten: server.py mit einem python3 Interpreter starten; der Server startet mit Standardeinstellungen (Port 5000)
Der Server hat keine Gui und kann nur gestartet und gestoppt werden.
Dann kann der client.py gestartet werden. 
Der Client hat GUIs, einmal für die Eingabe des Benutzernamens, dann der Server-IP und dem Port.

Wenn die Verbindung steht kann nun ein möglicher oder neuer Chat-Partner aufgerufen werden.
Im Chat kann man Nachrichten zu diesem Partner schicken, der Server speichert den Chatverlauf und die Chat-Partner in nachrichten.json
Diese Datei wird nur vom Server benutzt, der Client bekommt die Informationen über die socket-socket Verbindung geschickt.



server.py wurde von Fabio Kron geschrieben
auswahlGui.py, chatGui.py, client.py, nachrichtFormatter.py, nameGetGui.py, serverIP_Eingabe.py wurden von Hendrik Träber geschrieben
socketLib.py wurde von inf-schule.de übernommen (kleine Überarbeitungen waren nötig für die Funktionalität) 
