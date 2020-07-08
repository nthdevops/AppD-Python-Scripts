from xmlGenerator import xmlElements

x = xmlElements("test3.xml")
x.setTree("/templates/default.xml")
x.writeTree()