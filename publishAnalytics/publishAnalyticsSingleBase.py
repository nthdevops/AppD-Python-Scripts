import requests as req
import json
import os
import time

#Functions
def enviarRequisicao(url,headers,payload):
	res = req.post(url, headers=headers,data=payload)
	return res

def valorUnicoQuery(url,headers,payload):
	res = enviarRequisicao(url, headers, payload)
	resp = res.json()
	json_str = json.dumps(resp)
	jresp = json.loads(json_str)
	singleResult = (jresp[0]['results'][0][0])
	return int(singleResult)

def agregarValoresQueries(url,headers,queriesArray):
	somaTotal = 0
	for x in queriesArray:
		somaTotal += valorUnicoQuery(url,headers,x)
	return somaTotal

def tratarArray(array):
	newArray = []
	for x in array:
		newArray.append(x.rstrip())
	return newArray

def queriesArquivo(arquivo):
	#Abre o arquivo com as queries para os processos
	fp = open(os.getcwd()+arquivo)
	queries = fp.readlines()
	fp.close()
	queriesTratadas = tratarArray(queries)
	return queriesTratadas

#URLs
urlProdQuery = ("http://localhost:9080/events/query")
urlProdPublish = ("http://localhost:9080/events/publish/consolidBases")

#Headers
headersProdTxt = {
        "X-Events-API-AccountName":"customer1_59ea4341-3509-4b97-b1f8-542db8ca2e6a",
        "X-Events-API-Key":"407bddd1-77a7-4861-988e-0e2617463a7b",
        "Content-type":"application/vnd.appd.events+text;v=2"
}

headersProdJson = {
        "X-Events-API-AccountName":"customer1_59ea4341-3509-4b97-b1f8-542db8ca2e6a",
        "X-Events-API-Key":"407bddd1-77a7-4861-988e-0e2617463a7b",
        "Content-type":"application/vnd.appd.events+json;v=2"
}

#Payloads
queryValoresJaRegistrados = 'SELECT sum(total) FROM consolidBases WHERE dadosConsolidados = "seteProcessosChave"'
arq = '/seteProcesosChaveQs.txt'

#Requests
while True:
	print("Registrando dados")
	queriesTratadas = queriesArquivo(arq)
	valoresTotaisConsultados = agregarValoresQueries(urlProdQuery, headersProdTxt, queriesTratadas)
	totaisAtuais = valorUnicoQuery(urlProdQuery, headersProdTxt, queryValoresJaRegistrados)
	valorInsert = valoresTotaisConsultados - totaisAtuais
	pbStr = [{ 'dadosConsolidados': 'seteProcessosChave', 'total': valorInsert}]
	publishString = json.dumps(pbStr)

	if valorInsert > 0:
		rq = enviarRequisicao(urlProdPublish, headersProdJson, publishString)
		print(rq)
	else:
		print("Valor zero nao foi publicado")
	print("Proxima interacao em 60seg")
	time.sleep(60)