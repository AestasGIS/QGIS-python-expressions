from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsBlockingNetworkRequest, QgsProject, QgsCoordinateTransform, QgsCoordinateReferenceSystem
from json import loads 

# Opsæt koordinat system - objekter for hhv. QGIS projekt og for EPSG:25832 
ref_crs = QgsCoordinateReferenceSystem.fromEpsgId(25832)
proj_crs = QgsProject.instance().crs()

# Opsæt tekst skabelon for url kald 
url_tmpl = 'https://api.dataforsyningen.dk/adgangsadresser/reverse?x={}&y={}&srid=25832&struktur=flad'

# Find position for klik; denne er i projektets koordinatsystem
pnt = QgsPointXY(float([% @click_x %]), float([% @click_y %]))

# Tjek om projekt koordinatsystem er lig med EPSG:25832 (som er nødvendigt for DAWA request)
if proj_crs != ref_crs: 
    # Projekt koordinatsystem ikke 25832; transformér koordinat til 25832
    trns = QgsCoordinateTransform(proj_crs, ref_crs, QgsProject.instance())
    pnt2 = trns.transform(pnt)
else:
    pnt2 = pnt

# Opret url ud fra skabelon samt koordinat og opsæt request 
url = url_tmpl.format(pnt2.x(), pnt2.y())
request = QNetworkRequest(QUrl(url))

# Sæt max tid for request i millisekunder (sat til 0.5 sek) 
request.setTransferTimeout(500)

# Udfør request som en synkron "GET" request 
nam = QgsBlockingNetworkRequest()
nam.get(request, forceRefresh=True)
# Hent svar
reply = nam.reply()

# Ved succes (return code == 200) 
if reply.attribute(QNetworkRequest.HttpStatusCodeAttribute) == 200:
    
    # Hent resultat over i en streng variabel (json streng)
    content_string = reply.content().data().decode('utf8')
    
    # Konverter json streng til dict
    adress = loads(content_string)
    
    # Vis element 'betegnelse' i fra dict i messagebox
    QtWidgets.QMessageBox.information(None, "Adresse og matrikel", adress['betegnelse'] + '\n' + adress['matrikelnr'] + ' - ' + adress['ejerlavnavn'])

else:
    
    # Skriv fejlmeddelelse
    QtWidgets.QMessageBox.information(None, "Request fejl ", reply.errorString())
    


