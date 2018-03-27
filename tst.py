import pyyed
from xml.dom import minidom


g = pyyed.Graph()

g.add_node('foo',configuration="com.yworks.entityRelationship.big_entity",properties="aap\nnoot\nmies", width="200")
g.add_node('foo2', configuration="com.yworks.entityRelationship.small_entity")

g.add_edge('foo', 'foo2')
g.add_node('abc',  configuration="com.yworks.entityRelationship.relationship", modelName="custom")


g.add_edge('foo', 'abc', label="EDGE!")

#print(g.get_graph())

xmlstr = minidom.parseString(g.get_graph()).toprettyxml(indent="   ")
print(xmlstr)

with open("tst.graphml", "w") as f:
    f.write(xmlstr)

