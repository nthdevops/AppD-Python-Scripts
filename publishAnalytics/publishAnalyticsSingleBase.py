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

#URLs ONPREM
urlProdQuery = ("http://localhost:9080/events/query")
urlProdPublish = ("http://localhost:9080/events/publish/INSERIR_NOME_DA_BASE")

#Headers
headersProdTxt = {
        "X-Events-API-AccountName":"INSERIR",
        "X-Events-API-Key":"INSERIR",
        "Content-type":"application/vnd.appd.events+text;v=2"
}

headersProdJson = {
        "X-Events-API-AccountName":"INSERIR",
        "X-Events-API-Key":"INSERIR",
        "Content-type":"application/vnd.appd.events+json;v=2"
}

#Payloads
queryValoresJaRegistrados = 'SELECT sum(total) FROM INSERIR_NOME_DA_BASE WHERE INSERIR FILTROS DE CONTROLE
arq = '/ARQUIVO COM QUERIES PARA AS CONSULTAS DE CONSOLIDAÇÃO.txt'

#Requests
while True:
	print("Registrando dados")
	queriesTratadas = queriesArquivo(arq)
	valoresTotaisConsultados = agregarValoresQueries(urlProdQuery, headersProdTxt, queriesTratadas)
	totaisAtuais = valorUnicoQuery(urlProdQuery, headersProdTxt, queryValoresJaRegistrados)
	valorInsert = valoresTotaisConsultados - totaisAtuais
	pbStr = [{ 'FILTRO': 'CAMPO DE CONTROLE', 'total': valorInsert}]
	publishString = json.dumps(pbStr)

	if valorInsert > 0:
		rq = enviarRequisicao(urlProdPublish, headersProdJson, publishString)
		print(rq)
	else:
		print("Valor zero nao foi publicado")
	print("Proxima interacao em 60seg")
	time.sleep(60)