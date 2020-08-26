import requests, os
import xml.etree.cElementTree as ET

from importer import importerFixer
importerFixer.setImportPathRoot("../")
from csvToXmlDataCollector.appDXml.xmlGenerator import xmlElements

urls = {'applications':'https://raiadrogasilsa.saas.appdynamics.com/controller/rest/applications', 'genericAppAvail':'https://raiadrogasilsa.saas.appdynamics.com/controller/rest/applications/GENERICAPP/metric-data?metric-path=Application%20Infrastructure%20Performance%7C*%7CIndividual%20Nodes%7C*%7CAgent%7CApp%7CAvailability&time-range-type=BEFORE_NOW&duration-in-mins=15'}

def getFromController(url):
    return requests.get(url, auth=('serviceUser@raiadrogasilsa', 'serviceUser123'))

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