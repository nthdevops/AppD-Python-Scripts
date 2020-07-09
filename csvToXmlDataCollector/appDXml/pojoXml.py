from appDXml.xmlGenerator import xmlElements

class pojoXml(xmlElements):
	def __init__(self,filesRoot,file):
		super().__init__(filesRoot,file)
		self.__gathererTypes = {"return":"RETURN_VALUE_GATHERER_TYPE","index":"POSITION_GATHERER_TYPE"}
		self.__transformerTypes = {"toString":"TO_STRING_OBJECT_DATA_TRANSFORMER_TYPE","getterChain":"GETTER_METHODS_OBJECT_DATA_TRANSFORMER_TYPE"}
		self.__matchTypes = {"class":"MATCHES_CLASS"}

	def getGathererType(self,gathererType):
		return self.__gathererTypes[gathererType]

	def getTransformerType(self,transformerType):
		return self.__transformerTypes[transformerType]

	def getMatchType(self,matchType):
		return self.__matchTypes[matchType]

	def setDtGathererConfigElement(self):
		self.clearWorkingElements()
		el = self.getElementByTag("data-gatherer-configs")
		if el != None:
			self.addWorkingElement(el)

	def setAppDTsDStdTree(self,controllerVersionIn,mdsConfEnabledIn):
		self.setRoot("application")
		root = self.getRoot()
		self.setAttribute(root,"controller-version",controllerVersionIn)
		self.setAttribute(root,"mds-config-enabled",mdsConfEnabledIn)
		self.setSubElement(self.getRoot(),"data-gatherer-configs")
		self.setDtGathererConfigElement()

	def setPojoGatherer(self,attachNewBts,enableAnalytics,enableApm,dtName,classNameIn,methodNameIn):
		self.setCurrentElement("data-gatherer-configs")
		dtGC = self.getCurrentElement()
		pojoDt = self.setSubElement(dtGC,"pojo-data-gatherer-config")
		self.addWorkingElement(pojoDt)
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
		nameEnd = self.setSubElement(pojoDt,"name")
		nameEnd.text = dtName

	def addMethodInvocationGatherer(self,nameIn,positionIn,gathererTypeIn,transformerTypeIn,transformerValueIn):
		self.setCurrentElement("pojo-data-gatherer-config")
		pojoDt = self.getCurrentElement()
		methodInvocGatherer = self.setSubElement(pojoDt,"method-invocation-data-gatherer-config")
		name = self.setSubElement(methodInvocGatherer,"name")
		name.text = nameIn
		position = self.setSubElement(methodInvocGatherer,"position")
		position.text = positionIn
		gathererType = self.setSubElement(methodInvocGatherer,"gatherer-type")
		gathererType.text = self.getGathererType(gathererTypeIn)
		transformerType = self.setSubElement(methodInvocGatherer,"transformer-type")
		transformerType.text = self.getTransformerType(transformerTypeIn)
		if transformerTypeIn != "toString":
			transformerValue = self.setSubElement(methodInvocGatherer,"transformer-value")
			transformerValue.text = transformerValueIn