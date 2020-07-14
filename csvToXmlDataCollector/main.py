from appDXml.pojoXml import pojoXml
from appDXml.pojoElement import pojoElement
from appDCsv.csvToPojo import csvToPojo, csvReader
import os
import sys

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