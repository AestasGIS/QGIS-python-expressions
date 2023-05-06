# QGIS-python-expressions

Dette repository vil fremadrettet komme til at indeholder div. python kodestumper, som jeg benytter i forbindelse med QGIS. Indtil videre er der kun en kodestump for adresseopslag.

## Find adresse fra muse klik

Denne expression virker ved at definere en handling til et eller andet reference lag. Efter oprettelse kan funktionen aktiveres ved at aktivere "Kør objekthandling" (knap på værktøjslinjen, se fil "menu-line.PNG") og derefter klikke på et objekt fra reference laget. Funktionen vil derefter bruge koordinaten fra klikket og lave et opslag i DAWA's adresseregister og bruge svaret fra denne til at vise nærmeste adresse for klik positionen. 

Man bør vælge sit reference lag med omhu. Man kan jo kun klikke indenfor et eller andet referenceobjekt i laget, så laget bør være så "fladedækkende" som muligt, som f.eks. kommune polygoner. Selve klikket giver en nøjagtig koordinat, så søgningen på adresse er nøjagtig uanset størrelse og omfang af polygonerne i referencelaget.


Python koden er et relativt simpelt eksempel på at udføre en http request (REST) vha. QGIS og Python. Så den kan tilpasses til andre formål.

For at få denne expression til at virke.. 

1. På et referencelag tilføjes en "handling" - lagegenskaber, faneblad "Handlinger"; tryk på gønt kryds nederst i midten.
2. I "Type" vælges "Python" 
3. Sæt kryds i "Fang resultat" 
4. I "Formål med handling sættes kryds i "i "Kanvas". Evt. andre kryds fjernes
5. I "Handlings tekst" kopieres indholdet af fil "find_address_from_coordinate.py" ind.
6. Tryk på knap "Ok"

Se Screendump i fil "Coordinate_to address.PNG"
