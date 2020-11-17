#Relative import path fix
from importfix import importfix
importfix.setImportPathRoot("../")

import re
from appDCsv.csvReader import csvReader
from appDXml.pojoElement import pojoElement

class csvToPojo(csvReader):
	def __init__(self,filesRoot,csvFileName):
		delimiterChar = ";"
		self.__gathNames = []
		super().__init__(filesRoot,csvFileName,delimiterChar)

	def getAppRowsEmptyCellsAsMerges(self):
		csvRows = self.getCsvRows()
		returnRows = {}
		for c in range(0,len(csvRows)):
			if len(csvRows[c]) == 0:
				continue
			split = csvRows[c][4].split(",")
			newGat = ""
			for i in range(0,len(split)):
				split[i] = split[i].strip()
				if split[i] == "":
					split[i] = "toString"
				newGat += ","+split[i]
			newGat = newGat.replace(",","",1)
			csvRows[c][4] = newGat
			if c > 0:
				#Itera até 3, pois index 4 são os gatheres, que não devem ser alterados
				for count in range(0,4):
					csvRows[c][count] = csvRows[c][count].strip()
					if csvRows[c][count] == "":
						csvRows[c][count] = csvRows[c-1][count]
			if csvRows[c][0] in returnRows:
				returnRows[csvRows[c][0]].append(csvRows[c])
			else:
				returnRows.update({csvRows[c][0]:[csvRows[c]]})
		return returnRows

	def getAppRowsFullCheck(self):
		appRows = self.getAppRowsEmptyCellsAsMerges()
		#Para cada App
		for appKey in appRows:
			curApp = appRows[appKey]
			newCurApp = []
			dontIterate = []
			#Para cada pojo dentro da app
			for count in range(0,len(curApp)):
				#Caso o elemento tenha sido tratado, não iterar sobre
				if count in dontIterate:
					continue
				curArray = curApp[count]
				#Conta um pojo a frente em diante do pojo que está sendo analisado
				for countSub in range(count+1,len(curApp)):
					#Caso o elemento tenha sido tratado, não iterar sobre
					if countSub in dontIterate:
						continue
					subCurArray = curApp[countSub]
					#Campo 0 do Array = Application. Campo 2 do Array = Classe. Campo 3 do Array = Metodo
					if curArray[0] == subCurArray[0] and curArray[2] == subCurArray[2] and curArray[3] == subCurArray[3]:
						#Não irá iterar sobre este campo novamente
						dontIterate.append(countSub)
						#Campo 1 do Array = bts. Se não encontrou a bt, adiciona ela com vírgula
						bts = subCurArray[1].split(",")
						for bt in bts:
							if curArray[1].find(bt) == -1:
								curArray[1] += ","+bt
						#Campo 4 do Array = Gatherers. Se não encontrou o gatherer, adiciona ele com vírgula
						gatherers = subCurArray[4].split(",")
						for gt in gatherers:
							if gt.find(".") == 0:
								gt = gt.replace(".","",1)
							if curArray[4].find(gt) == -1:
								curArray[4] += ","+gt
				gatherers = curArray[4].split(",")
				for gatC in range(0,len(gatherers)):
					if gatherers[gatC] == '':
						gatherers[gatC].pop()
				curArray[4] = gatherers
				newCurApp.append(curArray)
			appRows[appKey] = newCurApp
		return appRows

	def gathName(self,nameIn):
		nameReturn = ""
		findArr = re.findall("[^get_][a-zA-Z0-9]{1,}",nameIn)
		nameReturn = nameIn if len(findArr) == 0 else findArr[0]
		return nameReturn

	def gathAutoNaming(self,*names):
		nameReturn = ""
		for name in names:
			if name != "":
				nameTemp = self.gathName(name)
				if nameReturn.find(name) == -1:
					nameReturn += "."+nameTemp if nameTemp != "param" else name
		return nameReturn

	def getParamIndex(self,paramText):
		indexArr = re.findall("\d{1,}", paramText)
		if len(indexArr) == 0:
			return 0
		else:
			return indexArr[0]

	def getCleanName(self,name):
		return ''.join(re.findall("[a-zA-Z0-9]{1,}",name))

	def pojoRowsFormat(self,checkCsv,prefix):
		appRows = None
		if checkCsv:
			appRows = self.getAppRowsFullCheck()
		else:
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
				dtName = self.getCleanName(prefix+""+dtClass.split(".")[-1]+"."+dtMethod)
				countDtName = self.getNameCountForApp(dtName,curApp,0)
				if(countDtName > 0):
					dtName = dtName+str(countDtName)
				curApp.update({dtName:{}})
				curDt = curApp[dtName]
				dtGatherersArray = dtRow[4]
				dtGatheres = {}
				for c in range(0,len(dtGatherersArray)):
					dtGatherersArray[c] = dtGatherersArray[c].strip()
					gatherersSplit = dtGatherersArray[c].split(".")
					gathererFirst = gatherersSplit[0]
					gathererLast = gatherersSplit[-1]
					gathererBeforeLast = gatherersSplit[-2] if len(gatherersSplit) > 1 else ""
					gathererName = prefix+key[0:4]
					position = 0
					gathererType = None
					transformerType = None
					transformerValue = None
					#Indica que é para index
					if gathererFirst.find("param") == 0:
						gathererType = "index"
						index = self.getParamIndex(gathererFirst)
						position = index
						#Indica que não tem getterChain, apenas toString
						if gathererFirst == gathererLast:
							gathererName += dtMethod+"."+gathererFirst
							transformerType = "toString"
						else:
							gathererName += dtMethod+self.gathAutoNaming(gathererBeforeLast,gathererLast)
							transformerType = "getterChain"
							transformerValueLessParam = dtGatherersArray[c].replace(gathererFirst+".", "")
							transformerValue = transformerValueLessParam.replace(".", "|")
					else:
						gathererType = "return"
						if gathererFirst == "toString" or gathererFirst == "" or gathererFirst == None:
							gathererName += dtMethod+".toString"
							transformerType = "toString"
						else:
							if gathererFirst != gathererLast:
								gathererName += dtMethod+self.gathAutoNaming(gathererBeforeLast,gathererLast)
							else:
								gathererName += dtMethod+self.gathAutoNaming(gathererLast)
							transformerType = "getterChain"
							transformerValue = dtGatherersArray[c].replace(".", "|")
					if transformerValue != None:
						findDoublePipe = re.findall("\|\|",transformerValue)
						if len(findDoublePipe) > 0:
							transformerValue = transformerValue.replace("||","|")
					gathererName = self.returnCheckedGathName(self.getCleanName(gathererName))
					dtGatheres.update({gathererName:{"position":position,"gathererType":gathererType,"transformerType":transformerType,"transformerValue":transformerValue}})
				curDt.update({'class':dtClass,'method':dtMethod,"bts":dtBts,"gatherers":dtGatheres})
		return formatedAppRows
	
	def getNameCountForApp(self,dtName,app,count):
		occurCount = 0
		cmpDtName = dtName
		if(count > 0):
			cmpDtName = dtName+str(count)
		for subDtName in app:
			if cmpDtName == subDtName:
				occurCount += 1
		totalCount = count+occurCount
		if occurCount > 0:
			totalCount = self.getNameCountForApp(dtName,app,totalCount)
		return totalCount

	def appPojoRowsToAppPojoElements(self,checkCsv,prefix):
		appPojoRows = self.pojoRowsFormat(checkCsv,prefix)
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

	def returnCheckedGathName(self, name):
		checkedGathName = name
		count = 1
		while checkedGathName in self.__gathNames:
			count += 1
			checkedGathName = name+str(count)

		if not (checkedGathName in self.__gathNames):
			self.__gathNames.append(checkedGathName)
		return checkedGathName