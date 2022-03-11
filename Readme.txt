*ANWENDUNG*

In diesem Ordner sind die notwendigen Skripte und Datensätze zur Ausführung des 
Histogramm-basierten LiDAR-Punktwolken-Generators enthalten.

Zum Ausführen des Generators muss das Skript "main" ausgeführt werden.
Dann öffnet sich die grafische Benutzeroberfläche des Generators.

Als nächstes müssen die Rate des Hintergrundlichtes und des reflektierten Lasers eingestellt werden.
Dann wird über "Choose Neural Network" ausgewählt, ob die klassische Verarbeitungsmethode oder die Methode
mit neuronalem Netz ausgewählt wird.
Danach wird mit "Choose Dataset" das entsprechende Szenario ausgewählt. Es öffnet sich ein Fenster, indem in den Ordnern
"Dynamic" und "Static" die jeweiligen Daten hinterlegt sind. In dem "Dynamic" Ordner befinden sich die Daten, bei denen
sich entweder das Fahrzeug oder die Person bewegen. In dem "Static" Ordner sind die statischen Daten hinterlegt, in
denen sich die Objekte nicht bewegen. Es muss dann eine der Text-Dateien ausgewählt werden.
Anschließend wird rechts daneben mit den Radiobuttons ausgewählt, ob das Modell des neuronalen Netzes mit oder 
ohne Hintergrundlicht-Unterdrückung verwendet werden soll und über den Button "Load NN weights" geladen.
!!!!!!!!!! AUCH WENN DIE KLASSISCHE METHODE GEWÄHLT WIRD, MUSS BEI DEN RADIOBUTTON EINE AUSWAHL GETROFFEN
WERDEN UND AUF "Load NN weights" GEDRÜCKT WERDEN. DIES HAT ABER KEINEN EFFEKT AUF DIE KLASSISCHE METHODE, IST 
ABER FÜR DAS FEHLERFREIE DURCHLAUFEN DES SIMULATORS ERFORDERLICH!!!!!!!!!

Rechts im Fenster "Run" kann dann der Generator über den Button "Run Generator" gestartet werden.
Die Durchführung der Simulation dauert einige Zeit.
Nach Durchführung der Simulation werden rechts unten Informationen dazu angezeigt. 
Diese Informationen können zusätzlich auch über den Button "Export Data" gespeichert werden. Sie befinden sich dann
in: "data -> generated_data -> parameters".

Über den Button "Visualize PC" können die Ground-Truth-Punktwolke des ausgewählten Szenarios und die Predicted-
Truth-Punktwolke mit den vorhergesagten Distanzen visualisiert werden.


--------------------------------------------------------------------------------------------------------
*ERWEITERUNG*

Veränderungen an der grafischen Benutzeroberfläche können in dem Skript "GUI" vorgenommen werden.

Das Skript "A_Datenerzeugung_Carla" wurde zum erzeugen der LiDAR-Simulation und der Szenarien verwendet. Um dies verwenden
zu können muss CARLA installiert werden. Hier wurde die CARLA-Version 0.9.11 verwendet.

Die weiteren Skripte mit der Bezeichnung "AA...", "AAA...", usw. sind die einzelnen Schritte die während der Durchführung
der Simulation mit dem Generator im Hintergrund ablaufen.

Das Skript "Evaluation" ist das Skript von Felix Landmeyer mit den Berechnungen für die klassische Methode und das 
neuronale Netz. Der Generator kann mit den noch weiteren hier vorhandenen Berechnungen erweitert werden, indem diese
mit dem Skript "AAAA_Prediction" verknüpft werden.


