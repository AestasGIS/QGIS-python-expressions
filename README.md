# QGIS-python-expressions

## Find adresse fra muse klik

Denne expression virker ved at definere en handling til et eller andet reference lag. Efter oprettelse kan funktionen aktiveres ved at vælge "Kør objekthandling" og klikke på et objekt fra reference laget. Funktionen vil derefter bruge koordinaten fra klikket og lave et opslag i DAWA's adresseregister og bruge svaret fra denne til at vise nærmeste adresse for klik positionen.


For at få denne expression til at virke.. 

1. På et referencelag tilføjes en "handling" - lagegenskaber, faneblad "Handlinger"; tryk på gønt kryds nederst i midten.
2. I "Type" vælges "Python" 
3. Sæt kryds i "Fang resultat" 
4. I "Formål med handling sættes kryds i "i "Kanvas"
5. I "Handlings tekst" kopieres indholdet af fil "find_address_from_coordinate.py" ind.
6. Tryk på knap "Ok"

Se Screendump i fil "Coordinate_to address.PNG"
