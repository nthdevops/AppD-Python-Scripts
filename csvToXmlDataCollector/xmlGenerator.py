import xml.etree.cElementTree as ET
import lxml.etree as etree
import os

class xmlElements(object):
	def __init__(self, file):
		self.__filesFolder = os.getcwd()+"/runtimeFiles"
		self.__file = file
		self.__fullPathFile = self.__filesFolder+"/"+file
		self.__root = ET.Element("empty")
		self.__workingElements.clear()

	def getFilesFolder(self):
		return self.__filesFolder

	def getFile(self):
		return self.__file

	def getFullPathFile(self):
		return self.__fullPathFile

	def getRoot(self):
		return self.__root

	def setRoot(self, rootName):
		self.__root = ET.Element(rootName)
		self.__workingElements.clear()

	def setWorkingElement(self, parent, subElementName):
		el = ET.SubElement(parent, subElementName)
		self.__workingElements.append(el)
		return el

	def setElementText(self, element, text):
		element.text = text

	def setAttribute(self, element, attr, value):
		element.set(attr, value)

	def getElementsByTag(self, root, elementTag):
		elements = []
		for child in root.iter(elementTag):
			elements.append(child)
		return elements

	def getElementByTextValue(self, root, elementText):
		element = ET.Element("empty").text = "empty"
		for child in root.iter(None):
			if(elementText == child.text):
				element = child
				break
		return element

	def getElementsByTextValue(self, root, elementText):
		elements = []
		for child in root.iter(None):
			if(elementText == child.text):
				elements.append(child)
		return element

	def getElementsByTag(self, elementTag):
		elements = []
		for child in self.__root.iter(elementTag):
			elements.append(child)
		return elements

	def getElementByTextValue(self, elementText):
		element = ET.Element("empty").text = "empty"
		for child in self.__root.iter(None):
			if(elementText == child.text):
				element = child
				break
		return element

	def printElementsTags(self, elements):
		for el in elements:
			print(el.tag)

	def writeTree(self):
		fullPathFile = self.__fullPathFile
		tree = ET.ElementTree(self.__root)
		tree.write(fullPathFile)
		x = etree.parse(fullPathFile)
		f = open(fullPathFile, "wb")
		f.write(etree.tostring(x, pretty_print=True))
		f.close()

	def setTree(self, filePathFromScriptPath):
		defaultPath = os.getcwd()
		filePath = defaultPath+filePathFromScriptPath
		self.__root = ET.parse(filePath).getroot()
		self.__workingElements.clear()
		for child in self.__root.iter(None):
			self.__workingElements.append(child)