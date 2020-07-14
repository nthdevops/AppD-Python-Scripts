import xml.etree.cElementTree as ET
import xml.dom.minidom
from lxml import etree
import os
from multipledispatch import dispatch

class xmlElements(object):
	def __init__(self,filesRoot,fileName):
		self.__filesFolder = filesRoot+"/runtimeFiles"
		self.__file = fileName+".xml"
		self.__fullPathFile = self.__filesFolder+"/"+self.getFile()
		self.__root = ET.Element("empty")
		self.__workingElements = {}
		self.__currentElement = None

	def getFilesFolder(self):
		return self.__filesFolder

	def getFile(self):
		return self.__file

	def getFullPathFile(self):
		return self.__fullPathFile

	def setRoot(self, rootName):
		self.__root = ET.Element(rootName)
		self.__workingElements.clear()

	def getRoot(self):
		return self.__root

	def addWorkingElement(self, element):
		self.__workingElements.update({element.tag:element})

	def getWorkingElement(self,elementName):
		element = self.__workingElements[elementName]
		return element

	def clearWorkingElements(self):
		self.__workingElements.clear()

	def leaveOnlyWorkingElement(self,onlyWorkingElementTag):
		onlyWorkingEl = self.setCurrentElement(onlyWorkingElementTag)
		self.__workingElements.clear()
		self.addWorkingElement(onlyWorkingEl)
		self.setCurrentElement(onlyWorkingEl)
		return self.getCurrentElement()

	@dispatch(str)
	def setCurrentElement(self, elementTag):
		el = self.getWorkingElement(elementTag)
		self.__currentElement = el
		return self.getCurrentElement()

	@dispatch(ET.Element)
	def setCurrentElement(self, element):
		self.__currentElement = element
		return self.getCurrentElement()

	def getCurrentElement(self):
		return self.__currentElement

	def setSubElement(self, parent, subElementName):
		el = ET.SubElement(parent, subElementName)
		return el

	def setAttribute(self, element, attr, value):
		element.set(attr, value)

	@dispatch(ET.Element,str)
	def getElementsByTag(self,root,elementTag):
		elements = []
		for child in root.iter(elementTag):
			elements.append(child)
		return elements

	@dispatch(str)
	def getElementsByTag(self,elementTag):
		elements = []
		for child in self.__root.iter(elementTag):
			elements.append(child)
		return elements

	@dispatch(str)
	def getElementByTag(self,elementTag):
		element = None
		for child in self.__root.iter(elementTag):
			element = child
			break
		return element

	@dispatch(ET.Element,str)
	def getElementByTag(self,root,elementTag):
		element = None
		for child in root.iter(elementTag):
			element = child
			break
		return element

	@dispatch(ET.Element,str)
	def getElementByTextValue(self,root,elementText):
		element = None
		for child in root.iter(None):
			if(elementText == child.text):
				element = child
				break
		return element

	@dispatch(str)
	def getElementByTextValue(self, elementText):
		element = None
		for child in self.__root.iter(None):
			if(elementText == child.text):
				element = child
				break
		return element

	def getElementsByTextValue(self, root, elementText):
		elements = None
		for child in root.iter(None):
			if(elementText == child.text):
				elements.append(child)
		return element

	def printElementsTags(self, elements):
		for el in elements:
			print(el.tag)

	def writeTree(self):
		fullPathFile = self.__fullPathFile
		tree = ET.ElementTree(self.__root)
		try:
			tree.write(fullPathFile)
			xmlStr = self.getCleanTreeStr(fullPathFile)
			dom = xml.dom.minidom.parseString(xmlStr)
			pretty = dom.toprettyxml()
			f = open(fullPathFile, "w")
			f.write(pretty)
			f.close()
			print("Arvore no arquivo "+fullPathFile)
		except Exception as e:
			print("Exception "+str(e)+" ao escrever arvore. Verifique se as libs estao instaladas e o arquivo atribuido esta correto.")

	def setTree(self, filePathFromScriptPath):
		defaultPath = os.getcwd()
		filePath = defaultPath+filePathFromScriptPath
		try:
			self.__root = ET.parse(filePath).getroot()
			self.__workingElements.clear()
		except Exception as e:
			print("Exception "+e+" ao ler arvore do arquivo. Verifique se as libs estao instaladas e o arquivo atribuido esta correto.")

	def getCleanTreeStr(self,filePath):
		tree = etree.parse(filePath)
		xmlStr = etree.tostring(tree.getroot())
		parser = etree.XMLParser(remove_blank_text=True)
		elem = etree.XML(xmlStr, parser=parser)
		return etree.tostring(elem)

	def getRootTreeFromStr(self,stringXml):
		return ET.fromstring(stringXml)

	def getRootFromFile(self,filePath):
		return self.getRootTreeFromStr(self.getCleanTreeStr(filePath))