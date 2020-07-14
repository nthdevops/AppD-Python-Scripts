from appDCsv.csvReader import csvReader
from appDXml.pojoElement import pojoElement
import re

class csvToPojo(csvReader):
	def __init__(self,filesRoot,csvFileName):
		delimiterChar = ";"
		super().__init__(filesRoot,csvFileName,delimiterChar)

	def pojoRowsFormat(self):
		appRows = self.getRowsDistinctColumn(0)
		formatedAppRows = {}
		#Itera sobre todas as apps retornadas
		for key in appRows:
			#Cria um dict element com a chave um dict vazio, salva na variavel cuApp qual o elemento de formatedAppRows sera alterado e qual os valores retornados dessa app pelo csv
			formatedAppRows.update({key:{}})
			curApp = formatedAppRows[key]
			curAppValue = appRows[key]
			#Pra cada array que venho de uma linha do csv faz a criação em pythonDict para criar os pojoElements futuramente
			for dtRow in curAppValue:
				dtBts = dtRow[1].split(",")
				for c in range(0,len(dtBts)):
					dtBts[c] = dtBts[c].strip()
				dtClass = dtRow[2]
				dtMethod = dtRow[3]
				dtName = dtClass.split(".")[-1]+"."+dtMethod
				curApp.update({dtName:{}})
				curDt = curApp[dtName]
				dtGatherersArray = dtRow[4].split(",")
				dtGatheres = {}
				for c in range(0,len(dtGatherersArray)):
					dtGatherersArray[c] = dtGatherersArray[c].strip()
					gathererFirst = dtGatherersArray[c].split(".")[0]
					gathererLast = dtGatherersArray[c].split(".")[-1]
					gathererName = None
					position = 0
					gathererType = None
					transformerType = None
					transformerValue = None
					#Indica que é para index
					if gathererFirst.find("param") == 0:
						gathererType = "index"
						index = re.findall("\d{1,}", gathererFirst)[0]
						position = index
						#Indica que não tem getterChain, apenas toString
						if gathererFirst == gathererLast:
							gathererName = dtMethod+"."+gathererFirst
							transformerType = "toString"
						else:
							gathererName = dtMethod+"."+gathererFirst+"."+gathererLast
							transformerType = "getterChain"
							transformerValueLessParam = dtGatherersArray[c].replace(gathererFirst+".", "")
							transformerValue = transformerValueLessParam.replace(".", "|")
					else:
						gathererType = "return"
						if gathererFirst == "toString":
							gathererName = dtMethod+".toString"
							transformerType = "toString"
						else:
							if gathererFirst != gathererLast:
								gathererName = dtMethod+"."+gathererFirst+"."+gathererLast
							else:
								gathererName = dtMethod+"."+gathererFirst
							transformerType = "getterChain"
							transformerValue = dtGatherersArray[c].replace(".", "|")
					dtGatheres.update({gathererName:{"position":position,"gathererType":gathererType,"transformerType":transformerType,"transformerValue":transformerValue}})
				curDt.update({'class':dtClass,'method':dtMethod,"bts":dtBts,"gatherers":dtGatheres})
		return formatedAppRows

	def appPojoRowsToAppPojoElements(self):
		appPojoRows = self.pojoRowsFormat()
		appPojoElements = {}
		for key in appPojoRows:
			appPojoElements.update({key:[]})
			curAppPojo = appPojoElements[key]
			curApp = appPojoRows[key]
			for pojoKey in curApp:
				pojoDict = curApp[pojoKey]
				pojoEl = pojoElement()
				dtName = pojoKey
				className = pojoDict["class"]
				methodName = pojoDict["method"]
				bts = pojoDict["bts"]
				pojoEl.setDefaultPojoGC(dtName,className,methodName,bts)
				gatherers = pojoDict["gatherers"]
				for gathererKey in gatherers:
					curGatherer = gatherers[gathererKey]
					name = gathererKey
					position = curGatherer["position"]
					gathererType = curGatherer["gathererType"]
					transformerType = curGatherer["transformerType"]
					transformerValue = curGatherer["transformerValue"]
					pojoEl.addPojoMethodInvocationGatherer(name,position,gathererType,transformerType,transformerValue)
				curAppPojo.append(pojoEl)
		return appPojoElements