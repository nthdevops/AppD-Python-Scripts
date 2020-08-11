import copy
import sys,os
from importer import importerFixer

importerFixer.setImportPathRoot("/../")
from appDXml.xmlGenerator import xmlElements
from appDXml.pojoElement import pojoElement
from multipledispatch import dispatch

class pojoXml(xmlElements):
	def __init__(self,filesRoot,fileToBeCreated,appName,getBts):
		super().__init__(filesRoot,fileToBeCreated)
		self.__gathererTypes = {"return":"RETURN_VALUE_GATHERER_TYPE","index":"POSITION_GATHERER_TYPE"}
		self.__transformerTypes = {"toString":"TO_STRING_OBJECT_DATA_TRANSFORMER_TYPE","getterChain":"GETTER_METHODS_OBJECT_DATA_TRANSFORMER_TYPE"}
		self.__matchTypes = {"class":"MATCHES_CLASS"}
		self.__getBts = getBts
		self.__applicationXmlFilePath = filesRoot+"/templates/"+appName+".xml"
		self.__btsNotFound = []
		if getBts:
			self.__appComponentsXmlTemplate = self.getBusinessTransactionsFromFile(self.__applicationXmlFilePath)

	def getGathererType(self,gathererType):
		return self.__gathererTypes[gathererType]

	def getBts(self):
		return self.__getBts

	def getTransformerType(self,transformerType):
		return self.__transformerTypes[transformerType]

	def getMatchType(self,matchType):
		return self.__matchTypes[matchType]

	def getBtsNotFound(self):
		return self.__btsNotFound

	def setBtNotFound(self,bt):
		self.__btsNotFound.append(bt)

	def setDtGathererConfigElement(self):
		self.clearWorkingElements()
		el = self.getElementByTag("data-gatherer-configs")
		if el != None:
			self.addWorkingElement(el)
		return self.setCurrentElement(el)

	def setAppDTsMinifiedDStdTree(self):
		self.setRoot("application")
		root = self.getRoot()
		self.setSubElement(root,"data-gatherer-configs")
		self.setDtGathererConfigElement()

	@dispatch(str,str,str,str,str,str)
	def setPojoGatherer(self,attachNewBts,enableAnalytics,enableApm,dtName,classNameIn,methodNameIn):
		dtGC = self.setDtGathererConfigElement()
		pojoDt = self.setSubElement(dtGC,"pojo-data-gatherer-config")
		self.addWorkingElement(pojoDt)
		self.setCurrentElement("pojo-data-gatherer-config")
		self.setAttribute(pojoDt,"attach-to-new-bts",attachNewBts)
		self.setAttribute(pojoDt,"enabled-for-analytics",enableAnalytics)
		self.setAttribute(pojoDt,"enabled-for-apm",enableApm)
		name = self.setSubElement(pojoDt,"name")
		name.text = dtName
		pojoMethodDef = self.setSubElement(pojoDt,"pojo-method-definition")
		self.addWorkingElement(pojoMethodDef)
		className = self.setSubElement(pojoMethodDef,"class-name")
		className.text = classNameIn
		methodName = self.setSubElement(pojoMethodDef,"method-name")
		methodName.text = methodNameIn
		matchName = self.setSubElement(pojoMethodDef,"match-type")
		matchName.text = self.getMatchType("class")
		self.setSubElement(pojoMethodDef,"method-parameter-types")

	def endPojo(self):
		pojoDt = self.getCurrentElement()
		dtName = self.getElementByTag(pojoDt,"name").text
		name = self.setSubElement(pojoDt,"name")
		name.text = dtName

	def addMethodInvocationGatherer(self,nameIn,positionIn,gathererTypeIn,transformerTypeIn,transformerValueIn):
		pojoDt = self.getCurrentElement()
		methodInvocGatherer = self.setSubElement(pojoDt,"method-invocation-data-gatherer-config")
		name = self.setSubElement(methodInvocGatherer,"name")
		name.text = nameIn
		position = self.setSubElement(methodInvocGatherer,"position")
		position.text = str(positionIn)
		gathererType = self.setSubElement(methodInvocGatherer,"gatherer-type")
		gathererType.text = self.getGathererType(gathererTypeIn)
		transformerType = self.setSubElement(methodInvocGatherer,"transformer-type")
		transformerType.text = self.getTransformerType(transformerTypeIn)
		if transformerTypeIn != "toString":
			transformerValue = self.setSubElement(methodInvocGatherer,"transformer-value")
			transformerValue.text = transformerValueIn

	def getAppInfos(self,filePath):
		root = self.getRootFromFile(filePath)
		controllerVersion = self.getAttribute(root,"controller-version")
		mdsEnable = self.getAttribute(root,"mds-config-enabled")
		return {"controllerVersion":controllerVersion,"mdsEnable":mdsEnable}

	@dispatch(pojoElement)
	def setPojoGatherer(self,pojoEl):
		if self.getRoot().tag == "empty":
			self.setAppDTsMinifiedDStdTree()
		pojoGathererConfig = pojoEl.getPojoGathererConfig()
		self.setPojoGatherer(pojoGathererConfig["attachNewBts"],pojoGathererConfig["enableAnalytics"],pojoGathererConfig["enableApm"],pojoGathererConfig["dtName"],pojoGathererConfig["className"],pojoGathererConfig["methodName"])
		pojoInvocGatheres = pojoEl.getPojoInvocationGatherers()
		for gatherer in pojoInvocGatheres:
			self.addMethodInvocationGatherer(gatherer["name"],gatherer["position"],gatherer["gathererType"],gatherer["transformerType"],gatherer["transformerValue"])
		self.endPojo()

	def setAppCompElement(self):
		self.clearWorkingElements()
		appC = self.getElementByTag("application-components")
		if appC != None:
			self.addWorkingElement(appC)
		return self.setCurrentElement(appC)

	def setAppBTsMinifiedDStdTree(self):
		self.setRoot("application")
		root = self.getRoot()
		attribs = self.getAppInfos(self.__applicationXmlFilePath)
		self.setAttribute(root,"controller-version",attribs["controllerVersion"])
		self.setAttribute(root,"mds-config-enabled",attribs["mdsEnable"])
		self.setSubElement(root,"data-gatherer-configs")
		self.setSubElement(root,"application-components")
		self.setAppCompElement()

	def getBusinessTransactionsFromFile(self,filePath):
		root = self.getRootFromFile(filePath)
		rootAppComps = self.getElementByTag(root,"application-components")
		appComps = self.getElementsByTag(rootAppComps,"application-component")
		returnComps = {}

		for appC in appComps:
			appCName = self.getElementByTag(appC,"name")
			if appCName == None:
				continue
			bssTrcs = self.getElementByTag(appC,"business-transactions")
			if bssTrcs != None:
				bssTrc = self.getElementsByTag(bssTrcs,"business-transaction")
				for bt in bssTrc:
					nameEl = self.getElementByTag(bt,"name")
					if nameEl != None:
						btName = nameEl.text
						if not appCName.text in returnComps:
							returnComps.update({appCName.text:{"appCompElement":appC,"bts":{}}})
						if btName == "_APPDYNAMICS_DEFAULT_TX_":
							btName = self.getAOTBtName(bt)
						bts = returnComps[appCName.text]["bts"]
						bts.update({btName:bt})
		return returnComps
	
	def getAOTBtName(self,bt):
		return "All Other Traffic - "+self.getElementByTag(bt,"application-component").text

	def getCleanAppComp(self,appC):
		if appC == None:
			print("Empty application-component.")
			return None
		appCCopy = self.getCopyLess(appC,"business-transactions")
		self.setSubElement(appCCopy,"business-transactions")
		return appCCopy

	def getAppComponent(self,appCompName):
		rootAppComps = self.getCurrentElement()
		appComps = self.getElementsByTag(rootAppComps,"application-component")
		appComp = None
		if not len(appComps) == 0:
			for appC in appComps:
				appCName = self.getElementByTag(appC,"name")
				if appCName == None:
					continue
				if appCName.text == appCompName:
					appComp = appC
					break
		return appComp

	def getBTFromTree(self,btName,appCompName):
		rootAppComps = self.getCurrentElement()
		appComps = self.getElementsByTag(rootAppComps,"application-component")
		btRet = None
		for appC in appComps:
			bssTrcs = self.getElementByTag(appC,"business-transactions")
			if bssTrcs != None:
				bssTrc = self.getElementsByTag(bssTrcs,"business-transaction")
				for bt in bssTrc:
					name = self.getElementByTag(bt,"name").text
					if name == "_APPDYNAMICS_DEFAULT_TX_":
						name = self.getAOTBtName(bt)
					if name.lower() == btName.lower():
						btRet = bt
						break
		return btRet

	def addDtToBT(self,appComponent,btElement,dtName):
		rootAppComps = self.getCurrentElement()
		appCompName = self.getElementByTag(appComponent,"name").text
		btName = self.getElementByTag(btElement,"name").text
		appComp = self.getAppComponent(appCompName)
		if appComp == None:
			appComp = self.getCleanAppComp(appComponent)
			self.setSubElement(rootAppComps,appComp)
		bt = self.getBTFromTree(btName,appCompName)
		if bt == None:
			bt = copy.deepcopy(btElement)
			bts = self.getElementByTag(appComp,"business-transactions")
			self.setSubElement(bts,bt)
		dtConfig = self.setSubElement(bt,"data-gatherer-config")
		dtConfig.text = dtName

	def setDataGatheresForBts(self,pojoEl):
		if self.getRoot().tag == "empty":
			self.setAppBTsMinifiedDStdTree()
		pojoBts = pojoEl.getPojoBts()
		pojoConfig = pojoEl.getPojoGathererConfig()
		for bt in pojoBts:
			btReturn = None
			for appCKey in self.__appComponentsXmlTemplate:
				appC = self.__appComponentsXmlTemplate[appCKey]
				bts = [x.lower() for x in appC["bts"]]
				if bt.lower() in bts:
					btReturn = bt
					index = bts.index(bt.lower())
					self.addDtToBT(appC["appCompElement"],list(appC["bts"].values())[index],pojoConfig["dtName"])
			if btReturn == None:
				if not bt in self.getBtsNotFound():
					self.setBtNotFound(bt)