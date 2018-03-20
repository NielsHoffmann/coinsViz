import pyyed

from rdflib import URIRef
from rdflib import Namespace

from rdflib.graph import Graph as rdfGraph

g = rdfGraph()
g.parse("/home/niels/Downloads/imgolf.rdf")


pg = pyyed.Graph()


print('nodes: ')
qres = g.query(
    """SELECT ?subject ?object
            WHERE {
                ?subject rdfs:subClassOf ?object .
                FILTER(STRSTARTS(STR(?object), "http://www.coinsweb.nl/cbim-2.0.rdf#"))
            }
    """)

for row in qres:
    print("%s is a %s" % row)
    try:
        pg.add_node(row[0].split('/')[-1])
    except:
        print(row[0].split('/')[-1])

print('edges: ')

# edges subclass rel
res = g.query(
    """
        SELECT ?subject ?object
            WHERE {
                ?subject rdfs:subClassOf ?object .
	            FILTER(STRSTARTS(STR(?object), "http://connecteddata.nl/coins/imgolf/"))
        }""")

for row2 in res:
    print("%s is a %s" % row2)
    pg.add_edge(row2[0].split('/')[-1],row2[1].split('/')[-1],label='subClassOf')


# edges contains rel
res2 = g.query(
    """
        SELECT ?subject ?object
            WHERE {
	            ?rel rdfs:subPropertyOf <http://www.coinsweb.nl/cbim-2.0.rdf#hasContainsRelation> .
	            ?rel rdfs:domain ?subject .
	            ?rel rdfs:range ?object .
        }""")

for row3 in res2:
    print("%s is a %s" % row3)
    pg.add_edge(row3[0].split('/')[-1],row3[1].split('/')[-1],label='ContainsRelation')


file = open("/home/niels/Downloads/imgolf.graphml",'w')
file.write( pg.get_graph())

file.close()
