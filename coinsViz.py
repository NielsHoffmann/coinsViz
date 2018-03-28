import pyyed
from SPARQLWrapper import SPARQLWrapper, JSON
from xml.dom import minidom
from optparse import OptionParser

# handle commandline options
usage = "usage: %prog -f outputfile -s sparqlendpoint -n namespace"
parser = OptionParser(usage=usage)
parser.add_option("-f", "--file", dest="filename",
                  help="outputfile (graphml)", metavar="FILE")
parser.add_option("-s", dest="sparqlendpoint",
                  help="sparqlendpoint om het model uit te analyseren")
parser.add_option("-n", "--Namespace", dest="namespace",
                  help="namespace van de objecten die in het model opgenomen moeten worden")

(options, args) = parser.parse_args()

# test op verplichte argumenten, alle argumenten zijn verplicht in dit geval
mandatories = ['filename', 'sparqlendpoint', 'namespace']
for m in mandatories:
    if not options.__dict__[m]:
        print "mandatory option is missing\n"
        parser.print_help()
        exit(-1)


pg = pyyed.Graph()

#sparql = SPARQLWrapper("http://localhost:7200/repositories/imgolf")
sparql = SPARQLWrapper(options.sparqlendpoint)
sparql.setReturnFormat(JSON)

#target_namespace = "http://connecteddata.nl/coins/imgolf/"
target_namespace = options.namespace

# alle cbim Objecten
node_query = ("""SELECT ?node
                WHERE {
    			?node rdfs:subClassOf+ <http://www.coinsweb.nl/cbim-2.0.rdf#Object> .
    			FILTER(STRSTARTS(STR(?node), "%s"))
				FILTER (!isBlank(?node))
                }""") % target_namespace

sparql.setQuery(node_query)
nodes = sparql.query().convert()

# vind de kenmerken voor cbim objecten
for node in nodes["results"]["bindings"]:
    nodename = node["node"]["value"]

    att_query = ("""SELECT ?att ?tp
            WHERE {
				?prop rdfs:subPropertyOf <http://www.coinsweb.nl/cbim-2.0.rdf#hasProperties> .
				?prop rdfs:domain <%s> .
				?prop rdfs:range ?att .
                ?att rdfs:subClassOf ?tp .
				FILTER(!STRSTARTS(STR(?tp), "http://www.coinsweb.nl/cbim-2.0.rdf#CataloguePart"))
				FILTER (!isBlank(?tp))
            }""") % nodename

    sparql.setQuery(att_query)
    atts = sparql.query().convert()
    lbl = ""
    for att in atts["results"]["bindings"]:
        attname = att["att"]["value"]
        atttype = att["tp"]["value"]

        if "#" in attname:
            attname = attname.split("#")[-1]
        elif "/" in attname:
            attname = attname.split("/")[-1]

        lbl = lbl + attname + " (" + atttype.split("#")[-1] + ") \n "

    try:
        if "#" in nodename:
            nodename = nodename.split("#")[-1]
        else:
            nodename = nodename.split("/")[-1]

        if lbl == "":  # small_entity
            pg.add_node(nodename, label=nodename, configuration="com.yworks.entityRelationship.small_entity")
        else:  # big_entity
            pg.add_node(nodename, label=nodename, configuration="com.yworks.entityRelationship.big_entity",
                        properties=lbl)
    except Exception as e:
        print("error adding node: " + nodename + e)

# relationship nodes
relnode_query = ("""SELECT ?node
                WHERE {
    			?node rdfs:subClassOf+ <http://www.coinsweb.nl/cbim-2.0.rdf#ContainsRelation> .
    			FILTER(STRSTARTS(STR(?node), "%s"))
				FILTER (!isBlank(?node))
                }""") % target_namespace

sparql.setQuery(relnode_query)
relnodes = sparql.query().convert()

for relnode in relnodes["results"]["bindings"]:
    relnodename = relnode["node"]["value"]

    if "#" in relnodename:
        relnodename = relnodename.split("#")[-1]
    else:
        relnodename = relnodename.split("/")[-1]

    pg.add_node(relnodename, label=relnodename, configuration="com.yworks.entityRelationship.relationship")

# edges subclass rel
rel_query = ("""SELECT ?subject ?object
                WHERE {
                ?subject rdfs:subClassOf+ ?object .
 	            FILTER(STRSTARTS(STR(?object), "%s"))
 	            FILTER(STRSTARTS(STR(?subject), "%s"))
                FILTER(!IsBlank(?subject))
                }""") % (target_namespace, target_namespace)
sparql.setQuery(rel_query)

edges = sparql.query().convert()
for edge in edges["results"]["bindings"]:
    edgefrom = edge["subject"]["value"]
    edgeto = edge["object"]["value"]

    if "#" in edgefrom:
        edgefrom = edgefrom.split("#")[-1]
    else:
        edgefrom = edgefrom.split("/")[-1]

    if "#" in edgeto:
        edgeto = edgeto.split("#")[-1]
    else:
        edgeto = edgeto.split("/")[-1]

    pg.add_edge(edgefrom, edgeto, label='subClassOf')

# edges contains rel
sparql.setQuery(""" SELECT ?subject ?object
                WHERE {
 	            ?rel rdfs:subPropertyOf <http://www.coinsweb.nl/cbim-2.0.rdf#hasContainsRelation> .
 	            ?rel rdfs:domain ?subject .
 	            ?rel rdfs:range ?object .
                }"""
                )

edges = sparql.query().convert()
for edge in edges["results"]["bindings"]:
    edgefrom = edge["subject"]["value"]
    edgeto = edge["object"]["value"]
    pg.add_edge(edgefrom.split('/')[-1], edgeto.split('/')[-1], label='ContainsRelation', arrowhead="none", arrowfoot="none")


xmlstr = minidom.parseString(pg.get_graph()).toprettyxml(indent="   ")

fname = options.filename
if not ".graphml" in fname:
    fname = fname + ".graphml"
with open(fname, "w") as f:
    f.write(xmlstr.encode('utf-8'))
