import os

class pojoElement(xmlElements):
	def __init__(self):
		self.__pojoGathererConfig["attachNewBts":None,"enableAnalytics":None,"enableApm":None,"dtName":None,"className":None,"methodName":None,"businessTransactions":None]
		self.__pojoMethodInvocationGathereres[]

	def setPojoGathererConfig(self,attachNewBts,enableAnalytics,enableApm,dtName,classNameIn,methodNameIn,bts):
		self.__pojoGathererConfig["attachNewBts"] = attachNewBts
		self.__pojoGathererConfig["enableAnalytics"] = enableAnalytics
		self.__pojoGathererConfig["enableApm"] = enableApm
		self.__pojoGathererConfig["dtName"] = dtName
		self.__pojoGathererConfig["className"] = classNameIn
		self.__pojoGathererConfig["methodName"] = methodNameIn
		self.__pojoGathererConfig["businessTransactions"] = bts

	def getPojoGathererConfig(self):
		return self.__pojoGathererConfig

	def getPojoBts(self):
		return self.getPojoGathererConfig()["businessTransactions"]

	def setPojoMethodInvocationGatherer(self,nameIn,positionIn,gathererTypeIn,transformerTypeIn,transformerValueIn):
		pojoInvocGat = {"name":nameIn,"position":positionIn,"gathererType":gathererTypeIn,"transformerType":transformerTypeIn,"transformerValue":transformerValueIn}
		self.__pojoMethodInvocationGathereres.append(pojoInvocGat)