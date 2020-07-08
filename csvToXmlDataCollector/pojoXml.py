from xmlGenerator import xmlElements

class pojoXml(xmlElements):
	def __init__(self, file):
		super().__init__(file)
		self.__gathererTypes = {"return":"RETURN_VALUE_GATHERER_TYPE","index":"POSITION_GATHERER_TYPE"}
		self.__transformerTypes = {"toString":"TO_STRING_OBJECT_DATA_TRANSFORMER_TYPE","getterChain":"GETTER_METHODS_OBJECT_DATA_TRANSFORMER_TYPE"}
		self.__matchTypes = {"class":"MATCHES_CLASS"}

	def getGathererType(self,gathererType):
		return self.__gathererTypes[gathererType]

	def getTransformerType(self,transformerType):
		return self.__transformerTypes[transformerType]

	def getMatchType(self,matchType):
		return self.__matchTypes[matchType]