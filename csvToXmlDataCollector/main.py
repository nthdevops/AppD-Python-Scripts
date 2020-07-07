from xmlGenerator import *

x = xmlElements("test2.xml")
x.setTree("/templates/default.xml")
x.setAttribute(x.getRoot(), 'controller-version', '004-005-006-007')
x.writeTree()