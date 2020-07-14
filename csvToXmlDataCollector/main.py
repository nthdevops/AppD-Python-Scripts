from appDXml.pojoXml import pojoXml
from appDXml.pojoElement import pojoElement
from appDCsv.csvToPojo import csvToPojo, csvReader
import os

rootPath = os.getcwd()
csvPojo = csvToPojo(rootPath,"appTest2.csv",";")
formatedPojo = csvPojo.pojoRowsFormat()
print(formatedPojo)


"""
bts1 = ["/login/auth","/user/loginTarget"]
bts2 = ["/dash/listNewReleases.json","/settings.json","/login/auth"]
gatheres1 = [{"nameIn":"Gatherer1","positionIn":"0","gathererTypeIn":"return","transformerTypeIn":"toString","transformerValueIn":None},{"nameIn":"Gatherer2","positionIn":"1","gathererTypeIn":"index","transformerTypeIn":"getterChain","transformerValueIn":"getPerson()|getCPF()"}]
gatheres2 = [{"nameIn":"Gatherer3","positionIn":"5","gathererTypeIn":"index","transformerTypeIn":"getterChain","transformerValueIn":"toInt()"},{"nameIn":"Gatherer4","positionIn":"0","gathererTypeIn":"return","transformerTypeIn":"toString","transformerValueIn":None}]

configs = [{"dtName":"PojoElement1","classNameIn":"com.class1","methodNameIn":"method1","bts":bts1,"gatheres":gatheres1},{"dtName":"PojoElement2","classNameIn":"com.class2","methodNameIn":"method2","bts":bts2,"gatheres":gatheres2}]
pjs = []

for conf in configs:
	pojoEl = pojoElement()
	pojoEl.setDefaultPojoGC(conf["dtName"],conf["classNameIn"],conf["methodNameIn"],conf["bts"])
	for gatherer in conf["gatheres"]:
		pojoEl.addPojoMethodInvocationGatherer(gatherer["nameIn"],gatherer["positionIn"],gatherer["gathererTypeIn"],gatherer["transformerTypeIn"],gatherer["transformerValueIn"])
	pjs.append(pojoEl)

p = pojoXml(os.getcwd(),"testPojoElement","Tibco")
for pojoEl in pjs:
	p.setPojoGatherer(pojoEl)
p.writeTree()
"""
"""
p.setPojoGatherer("true","true","true","Final test XML","com.br.class1","method1")
p.addMethodInvocationGatherer("testReturnToString","0","return","toString",None)
p.addMethodInvocationGatherer("testIndexGetterChain","0","index","getterChain","getPerson()|toList()[0]")
"""