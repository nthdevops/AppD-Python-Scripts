from appDXml.pojoXml import pojoXml
from appDXml.pojoElement import pojoElement
from appDCsv.csvToPojo import csvToPojo, csvReader
import os
import sys

if not os.path.isdir("./runtimeFiles"):
	os.mkdir("./runtimeFiles")
if not os.path.isdir("./templates"):
	print("Pasta templates não encontrada, reveja o arquivo README para execução correta do script")
	sys.exit()

rootPath = os.getcwd()
csvFile = sys.argv[1]
csvPojo = csvToPojo(rootPath,csvFile)
appPojoElements = csvPojo.appPojoRowsToAppPojoElements()
for appKey in appPojoElements:
	p = pojoXml(os.getcwd(),appKey+"_appDDtsConfig",appKey)
	pojos = appPojoElements[appKey]
	for pojoEl in pojos:
		p.setPojoGatherer(pojoEl)
	p.writeTree()