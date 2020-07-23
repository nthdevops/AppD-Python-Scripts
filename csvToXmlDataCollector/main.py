import os,sys
root = os.getcwd()
os.chdir(root+"/../")
sys.path.append(os.getcwd())
os.chdir(root)
from appDXml.pojoXml import pojoXml
from appDXml.pojoElement import pojoElement
from appDCsv.csvToPojo import csvToPojo, csvReader

def strBool(v):
  return v.lower() in ("yes", "true", "t", "1")

if not os.path.isdir("./runtimeFiles"):
	os.mkdir("./runtimeFiles")
if not os.path.isdir("./templates"):
	print("Pasta templates não encontrada, reveja o arquivo README para execução correta do script")
	sys.exit()

rootPath = os.getcwd()
csvFile = sys.argv[1]
checkCsv = strBool(sys.argv[2])
getDTS = strBool(sys.argv[3])
getBts = strBool(sys.argv[4])
csvPojo = csvToPojo(rootPath,csvFile)
print("\nColetando dados do CSV\n")
appPojoElements = csvPojo.appPojoRowsToAppPojoElements(checkCsv)
for appKey in appPojoElements:
	pojos = appPojoElements[appKey]
	dtsNum = 1
	btsNum = 1
	maxLines = 10000
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
			if p.getXmlSize() > maxLines:
					btsNum +=1
					print("NAO ENCONTRADAS: "+str(p.getBtsNotFound())+"\n")
					p.writeTree()
					print()
					p = pojoXml(os.getcwd(),appKey+"_BusinessTransactions"+str(btsNum),appKey,getBts)
			p.setDataGatheresForBts(pojoEl)
		if len(p.getBtsNotFound()) > 0:
			print("NAO ENCONTRADAS: "+str(p.getBtsNotFound())+"\n")
		p.writeTree()
		print()