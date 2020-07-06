import xml.etree.cElementTree as ET
import lxml.etree as etree
import os

scriptPath = os.getcwd()
file = "xmlTest.xml"
fullPathFile = scriptPath+"/"+file
root = ET.Element("root")
doc = ET.SubElement(root, "doc")

ET.SubElement(doc, "field1", name="blah").text = "some value1"
ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

tree = ET.ElementTree(root)
tree.write(fullPathFile)


x = etree.parse(fullPathFile)
f = open(fullPathFile, "wb")
f.write(etree.tostring(x, pretty_print=True))
f.close()