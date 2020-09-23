import requests, os, configparser

from importer import importerFixer
importerFixer.setImportPathRoot("../")
from csvToXmlDataCollector.appDXml.xmlGenerator import xmlElements

config = configparser.ConfigParser()

config.read('example.ini')

def getFromController(url):
    return requests.get(url, auth=('USUARIO@ACCOUNT', 'SENHA'))

def getAppInfo(appName):
    url = urls['genericAppAvail'].replace('GENERICAPP',appName)
    return getFromController(url)

xmlApps = xmlElements(os.getcwd(),'applications')

resp = getFromController(urls['applications'])

xmlApps.setRootFromStr(resp.text)
appNames = [name.text for name in xmlApps.getElementsByTag('name')]
appsXmls = []
for app in appNames:
    appXml = getAppInfo(app).text
    appsXmls.append(appXml)
    xmlApps = xmlElements(os.getcwd(),app)
    xmlApps.setRootFromStr(appXml)
    xmlApps.writeTree()