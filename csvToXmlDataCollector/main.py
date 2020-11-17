# -*- coding: utf-8 -*-
#Relative fix
from importfix import importfix
importfix.setImportPathRoot("../")

#Local
from appDXml.pojoXml import pojoXml
from appDXml.pojoElement import pojoElement
from appDCsv.csvToPojo import csvToPojo, csvReader

#Packages
import os,sys

def strBool(v):
  return v.lower() in ("yes", "true", "t", "1")

if not os.path.isdir("./runtimeFiles"):
	os.mkdir("./runtimeFiles")
if not os.path.isdir("./templates"):
	print("Pasta templates não encontrada, reveja o arquivo README para execução correta do script")
	sys.exit()

if len(sys.argv) < 6:
	print("Argumentos de entrada incompletos!")
	sys.exit()

rootPath = os.getcwd()
csvFile = sys.argv[1]
prefix = sys.argv[2]
checkCsv = strBool(sys.argv[3])
getDTS = strBool(sys.argv[4])
getBts = strBool(sys.argv[5])
csvPojo = csvToPojo(rootPath,csvFile)
print("\nColetando dados do CSV\n")
appPojoElements = csvPojo.appPojoRowsToAppPojoElements(checkCsv,prefix)
for appKey in appPojoElements:
	pojos = appPojoElements[appKey]
	dtsNum = 1
	btsNum = 1
	maxLines = 45000
	if getDTS:
		print("Processando data collectors para a application "+appKey+"\n")
		print()
		p = pojoXml(os.getcwd(),appKey+"_DataCollectors",appKey,getBts)
		for pojoEl in pojos:
				if p.getXmlSize() > maxLines:
					dtsNum +=1
					p.writeTree()
					print()
					p = pojoXml(os.getcwd(),appKey+"_DataCollectors"+str(dtsNum),appKey,getBts)
				p.setPojoGatherer(pojoEl)
		p.writeTree()
		print()
	if getBts:
		print("Processando business transactions para a application "+appKey+"\n")
		p = pojoXml(os.getcwd(),appKey+"_BusinessTransactions",appKey,getBts)
		for pojoEl in pojos:
			p.setDataGatheresForBts(pojoEl)
		if len(p.getBtsNotFound()) > 0:
			print("NAO ENCONTRADAS: "+str(p.getBtsNotFound())+"\n")
		p.writeTree()
		print()