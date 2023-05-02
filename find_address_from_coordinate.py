from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsBlockingNetworkRequest, QgsProject, QgsCoordinateTransform, QgsCoordinateReferenceSystem
from json import loads 

ref_crs = QgsCoordinateReferenceSystem.fromEpsgId(25832)
proj_crs = QgsProject.instance().crs()

url_tmpl = 'https://api.dataforsyningen.dk/adgangsadresser/reverse?x={}&y={}&srid=25832&struktur=mini'


pnt = QgsPointXY(float([% @click_x %]), float([% @click_y %]))

if proj_crs != ref_crs: 
    trns = QgsCoordinateTransform(proj_crs, ref_crs, QgsProject.instance())
    pnt2 = trns.transform(pnt)
else:
    pnt2 = pnt

url = url_tmpl.format(pnt2.x(), pnt2.y())
request = QNetworkRequest(QUrl(url))

nam = QgsBlockingNetworkRequest()
nam.get(request, forceRefresh=True)
reply = nam.reply()

if reply.attribute(QNetworkRequest.HttpStatusCodeAttribute) == 200:
    content_string = reply.content().data().decode('utf8')
    adress = loads(content_string)
    QtWidgets.QMessageBox.information(None, "Adresse", adress['betegnelse'])



