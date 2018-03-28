# coinsViz
Visualisatie tooltje om COINS OTL's in graphml uit te drukken

De OTL moet via een sparql endpoint te benaderen zijn. 
De gegenereerde graphml file kan vervolgens met yEd getoond worden.
Er wordt specifieke opmaak geschreven in de graphml file voor yEd.

De python code gebruikt SPARQLWrapper en een aangepaste versie van pyyed.
De aangepaste pyyed module is te vinden op: https://github.com/provincieNH/pyyed

De module kan via de commandline gebruikt worden met de volgende parameters:

```
Usage: coinsViz.py -f outputfile -s sparqlendpoint -n namespace

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  outputfile (graphml)
  -s SPARQLENDPOINT     sparqlendpoint om het model uit te analyseren
  -n NAMESPACE, --Namespace=NAMESPACE
                        namespace van de objecten die in het model opgenomen
                        moeten worden
```

In yEd kan vervolgens vis het Layout menu de gewenste visualisatie van het diagram gekozen worden.
Als voorbeeld bevat deze repository een tst.graphml file en een imgolf.graphml file.

![imgolf](https://github.com/provincieNH/coinsViz/blob/master/imgolf.png)
