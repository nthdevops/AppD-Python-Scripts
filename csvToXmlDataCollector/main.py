from appDXml.pojoXml import pojoXml
import os

p = pojoXml(os.getcwd(),"testFinal.xml")
p.setAppDTsDStdTree("020-004-003-000","true")
p.setPojoGatherer("true","true","true","Final test XML","com.br.class1","method1")
p.addMethodInvocationGatherer("testReturnToString","0","return","toString",None)
p.addMethodInvocationGatherer("testIndexGetterChain","0","index","getterChain","getPerson()|toList()[0]")
p.writeTree()