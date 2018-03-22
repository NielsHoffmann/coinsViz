import pyyed

from rdflib import URIRef
from rdflib import Namespace
from SPARQLWrapper import SPARQLWrapper,JSON

from rdflib.graph import Graph as rdfGraph

g = rdfGraph()
g.parse("/home/niels/tmp/IMGolf-coins.ttl", format='turtle')


pg = pyyed.Graph()

sparql = SPARQLWrapper("http://100.115.92.1:7200/repositories/imgolf")

sparql.setQuery("""SELECT ?att ?tp
            WHERE {
				?prop rdfs:subPropertyOf <http://www.coinsweb.nl/cbim-2.0.rdf#hasProperties> .
				?prop rdfs:domain <http://connecteddata.nl/coins/imgolf/Golfbaan> .
				?prop rdfs:range ?att .
                ?att rdfs:subClassOf ?tp .
				?tp rdfs:subClassOf+ <http://www.coinsweb.nl/cbim-2.0.rdf#SimpleProperty> .
				FILTER (!isBlank(?tp))
            }""")


sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    #print(result["att"]["tp"])
    print(result)

# print('nodes: ')
# #qres = g.query(
# #    """SELECT ?subject ?object
# #            WHERE {
# #                ?subject rdfs:subClassOf ?object .
# #                FILTER(STRSTARTS(STR(?object), "http://www.coinsweb.nl/cbim-2.0.rdf#"))
# #            }
# #    """)
#
# # qres = g.query("""SELECT ?subject ?object WHERE{
# #     {
# # 	    SELECT ?subject ?object
# #             WHERE {
# #                 ?subject rdfs:subClassOf ?object .
# #                 FILTER(STRSTARTS(STR(?object), "http://www.coinsweb.nl/cbim-2.0.rdf#"))
# #     }
# #     }
# #     UNION
# #     {
# #         SELECT ?subject WHERE
# #         {?subject rdfs:label 'Golfbaan' .}
# #     }}""")
#
# qres = g.query(""" SELECT ?subject WHERE
#         {?subject rdfs:label 'Golfbaan' .}""")
#
# for row in qres:
#     #print("%s is a %s" % row)
#     nodename=row[0]
#     #node labels
#
#     qry = ("""SELECT ?att ?t
#             WHERE {
# 				?prop rdfs:subPropertyOf <http://www.coinsweb.nl/cbim-2.0.rdf#hasProperties> .
# 				?prop rdfs:domain <%s> .
# 				?prop rdfs:range ?att .
#                 ?att rdfs:subClassOf ?t .
# 				?t rdfs:subClassOf+ <http://www.coinsweb.nl/cbim-2.0.rdf#SimpleProperty> .
#             }""") % nodename
#
#     print('query is: '+qry)
#
#     q = g.query(qry
#
#     )
#
#     lbl=""
#     for r in q:
#         lbl=r[0].split('/')[-1] + "(" + r[1].split('#')[-1]+") /n"
#
#
#     try:
#         pg.add_node(nodename.split('/')[-1], label=nodename.split('/')[-1] + "/n"+ lbl)
#     except:
#         print(row[0].split('/')[-1])
#
#
#
# print('edges: ')
#
# # edges subclass rel
# res = g.query(
#     """
#         SELECT ?subject ?object
#             WHERE {
#                 ?subject rdfs:subClassOf ?object .
# 	            FILTER(STRSTARTS(STR(?object), "http://connecteddata.nl/coins/imgolf/"))
#         }""")
#
# for row2 in res:
#     print("%s is a %s" % row2)
#     pg.add_edge(row2[0].split('/')[-1],row2[1].split('/')[-1],label='subClassOf')
#
#
# # edges contains rel
# res2 = g.query(
#     """
#         SELECT ?subject ?object
#             WHERE {
# 	            ?rel rdfs:subPropertyOf <http://www.coinsweb.nl/cbim-2.0.rdf#hasContainsRelation> .
# 	            ?rel rdfs:domain ?subject .
# 	            ?rel rdfs:range ?object .
#         }""")
#
# for row3 in res2:
#     print("%s is a %s" % row3)
#     pg.add_edge(row3[0].split('/')[-1],row3[1].split('/')[-1],label='ContainsRelation')
#
#
# file = open("/home/niels/tmp/imgolf.graphml",'w')
# file.write( pg.get_graph())
#
# file.close()
