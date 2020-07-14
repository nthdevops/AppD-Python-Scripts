import os

class pojoElement(object):
	def __init__(self):
		self.__pojoGathererConfig = {"attachNewBts":None,"enableAnalytics":None,"enableApm":None,"dtName":None,"className":None,"methodName":None,"businessTransactions":None}
		self.__pojoMethodInvocationGathereres = []

	def setPojoConf(self,configField,value):
		self.__pojoGathererConfig[configField] = value

	def setPojoGathererConfig(self,attachNewBts,enableAnalytics,enableApm,dtName,classNameIn,methodNameIn,bts):
		self.setPojoConf("attachNewBts",attachNewBts)
		self.setPojoConf("enableAnalytics",enableAnalytics)
		self.setPojoConf("enableApm",enableApm)
		self.setPojoConf("dtName",dtName)
		self.setPojoConf("className",classNameIn)
		self.setPojoConf("methodName",methodNameIn)
		self.setPojoConf("businessTransactions",bts)

	def setDefaultPojoGC(self,dtName,classNameIn,methodNameIn,bts):
		self.setPojoGathererConfig("false","true","false",dtName,classNameIn,methodNameIn,bts)

	def getPojoGathererConfig(self):
		return self.__pojoGathererConfig

	def getPojoInvocationGatherers(self):
		return self.__pojoMethodInvocationGathereres

	def getPojoBts(self):
		return self.getPojoGathererConfig()["businessTransactions"]

	def addPojoMethodInvocationGatherer(self,nameIn,positionIn,gathererTypeIn,transformerTypeIn,transformerValueIn):
		pojoInvocGat = {"name":nameIn,"position":positionIn,"gathererType":gathererTypeIn,"transformerType":transformerTypeIn,"transformerValue":transformerValueIn}
		self.__pojoMethodInvocationGathereres.append(pojoInvocGat)