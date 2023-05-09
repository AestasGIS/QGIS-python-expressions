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
    QtWidgets.QMessageBox.information(None, "Adresse og matrikel", adress['betegnelse'] + '\n' + adress['matrikelnr'] + '; ' + adress['ejerlavnavn'])
    # Andre mulige oplysninger og der er mange flere
"""
Andre oplysninger...
{
  "id": "0a3f507a-b2e6-32b8-e044-0003ba298018",
  "status": 1,
  "darstatus": 3,
  "oprettet": "2000-02-05T20:17:47.000",
  "ændret": "2019-07-12T05:56:50.651",
  "vejkode": "4112",
  "vejnavn": "Landgreven",
  "adresseringsvejnavn": "Landgreven",
  "husnr": "10",
  "supplerendebynavn": null,
  "postnr": "1301",
  "postnrnavn": "København K",
  "stormodtagerpostnr": null,
  "stormodtagerpostnrnavn": null,
  "kommunekode": "0101",
  "kommunenavn": "København",
  "ejerlavkode": 2000166,
  "ejerlavnavn": "Sankt Annæ Vester Kvarter, København",
  "matrikelnr": "7000æ",
  "esrejendomsnr": "22039",
  "etrs89koordinat_øst": 725369.59,
  "etrs89koordinat_nord": 6176652.55,
  "wgs84koordinat_bredde": 55.68323838,
  "wgs84koordinat_længde": 12.5851472,
  "nøjagtighed": "A",
  "kilde": 5,
  "tekniskstandard": "TD",
  "tekstretning": 200,
  "adressepunktændringsdato": "2002-04-05T00:00:00.000",
  "ddkn_m100": "100m_61766_7253",
  "ddkn_km1": "1km_6176_725",
  "ddkn_km10": "10km_617_72",
  "regionskode": "1084",
  "regionsnavn": "Region Hovedstaden",
  "jordstykke_ejerlavkode": 2000166,
  "jordstykke_matrikelnr": "7000æ",
  "jordstykke_esrejendomsnr": "22039",
  "jordstykke_ejerlavnavn": "Sankt Annæ Vester Kvarter, København",
  "højde": 4,
  "adgangspunktid": "0a3f507a-b2e6-32b8-e044-0003ba298018",
  "vejpunkt_id": "11e4ae5e-af45-11e7-847e-066cff24d637",
  "vejpunkt_kilde": "Ekstern",
  "vejpunkt_nøjagtighed": "B",
  "vejpunkt_tekniskstandard": "V0",
  "vejpunkt_x": 12.58506685,
  "vejpunkt_y": 55.68314226,
  "sognekode": "7037",
  "sognenavn": "Garnisons",
  "politikredskode": "1470",
  "politikredsnavn": "Københavns Politi",
  "retskredskode": "1101",
  "retskredsnavn": "Københavns Byret",
  "opstillingskredskode": "0003",
  "opstillingskredsnavn": "Indre By",
  "menighedsrådsafstemningsområdenummer": 11,
  "menighedsrådsafstemningsområdenavn": "Garnisons",
  "zone": "Byzone",
  "afstemningsområdenummer": "14",
  "afstemningsområdenavn": "3. Øst",
  "brofast": true,
  "supplerendebynavn_dagi_id": null,
  "navngivenvej_id": "7be9be74-d2cf-4cd1-8b75-cbaaf47cb5a9",
  "vejpunkt_ændret": "2018-05-03T14:08:02.125",
  "ikrafttrædelse": "2000-02-05T20:17:47.000",
  "nedlagt": null,
  "storkredsnummer": "1",
  "storkredsnavn": "København",
  "valglandsdelsbogstav": "A",
  "valglandsdelsnavn": "Hovedstaden",
  "landsdelsnuts3": "DK011",
  "landsdelsnavn": "Byen København",
  "betegnelse": "Landgreven 10, 1301 København K", <--- Det er den som pt. bruges
  "kvh": "01014112__10"
}
"""
else:
    
    # Skriv fejlmeddelelse
    QtWidgets.QMessageBox.information(None, "Request fejl ", reply.errorString())
    


