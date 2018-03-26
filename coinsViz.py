import pyyed

from rdflib import URIRef
from rdflib import Namespace
from SPARQLWrapper import SPARQLWrapper,JSON


pg = pyyed.Graph()

sparql = SPARQLWrapper("http://localhost:7200/repositories/imgolf")
sparql.setReturnFormat(JSON)

target_namespace = "http://connecteddata.nl/coins/imgolf/"

node_query = ("""SELECT ?node
                WHERE {
    			?node rdfs:subClassOf+ <http://www.coinsweb.nl/cbim-2.0.rdf#Object> .
    			FILTER(STRSTARTS(STR(?node), "%s"))
				FILTER (!isBlank(?node))
                }""") % target_namespace

print(node_query)

#nodes
sparql.setQuery(node_query)

nodes =  sparql.query().convert()
for node in nodes["results"]["bindings"]:
    nodename = node["node"]["value"]
    #print(node["node"]["value"])

    att_query = ("""SELECT ?att ?tp
            WHERE {
				?prop rdfs:subPropertyOf <http://www.coinsweb.nl/cbim-2.0.rdf#hasProperties> .
				?prop rdfs:domain <%s> .
				?prop rdfs:range ?att .
                ?att rdfs:subClassOf ?tp .
				?tp rdfs:subClassOf+ <http://www.coinsweb.nl/cbim-2.0.rdf#SimpleProperty> .
				FILTER (!isBlank(?tp))
            }""") % nodename

    sparql.setQuery(att_query)
    atts = sparql.query().convert()
    lbl=""
    for att in atts["results"]["bindings"]:
        attname = att["att"]["value"]
        atttype = att["tp"]["value"]
        #print(attname + " is van type: " + atttype)

        if "#" in attname:
            attname = attname.split("#")[-1]
        else:
            attname = attname.split("/")[-1]

        lbl = lbl + attname + " (" + atttype.split("#")[-1] + ") \n "

    try:
        if "#" in nodename:
            nodename = nodename.split("#")[-1]
        else:
            nodename = nodename.split("/")[-1]

        pg.add_node(nodename, label=nodename + " \n" + lbl)
    except:
        print("error adding node: " + nodename)

#edges subclass rel
rel_query = ("""SELECT ?subject ?object
                WHERE {
                ?subject rdfs:subClassOf+ ?object .
 	            FILTER(STRSTARTS(STR(?object), "%s"))
                FILTER(!IsBlank(?subject))
                }""") % target_namespace
sparql.setQuery(rel_query)

edges = sparql.query().convert()
for edge in edges["results"]["bindings"]:
    edgefrom = edge["subject"]["value"]
    edgeto = edge["object"]["value"]
    pg.add_edge(edgefrom.split('/')[-1], edgeto.split('/')[-1], label='subClassOf')



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
    pg.add_edge(edgefrom.split('/')[-1], edgeto.split('/')[-1], label='ContainsRelation')



file = open("d:/tmp/imgolf.graphml",'w')
file.write(pg.get_graph())

file.close()
