#Relative import path fix
from importfix import importfix
importfix.setImportPathRoot("../")

#Local imports
from csvToXmlDataCollector.appDXml.xmlGenerator import xmlElements
from SaaSKeepAlive.controller import controller
from SaaSKeepAlive.customLogs import logger

#Package imports
import os

iniPath = './appd_config.ini'
ctl = controller(iniPath)
logs = logger(iniPath,'main',True)

xmlApps = xmlElements('applications')

applicationsXml = ctl.requestController(ctl.getUrl('applications')).text

xmlApps.setRootFromStr(applicationsXml)
appNames = [name.text for name in xmlApps.getElementsByTag('name')]
totalNodes = 0
totalAvailCount = 0
for app in appNames:
    logs.write('Processing App: '+app,'INFO')
    appXml = ctl.getAppResponse(app).text
    xmlApps = xmlElements(app)
    xmlApps.setRootFromStr(appXml)
    metricValues = xmlApps.getElementsByTag('metricValues')
    for el in metricValues:
        totalNodes += 1
        metric = xmlApps.getElementByTag(el,'metric-value')
        if metric != None:
            totalAvailCount += int(xmlApps.getElementByTag(metric,'count').text)
        else:
            logs.write('15 min unavailable node for app '+app,'DEBUG')

totalAvailExpected = totalNodes * 15
percentAvail = (totalAvailCount * 100) / totalAvailExpected
logs.write('TotalNodes: '+str(totalNodes)+' | Availability Expected: '+str(totalAvailExpected)+' | Availability: '+str(totalAvailCount)+' | Percent: '+str(percentAvail)+'%','INFO')
logs.write('Finished processing!','INFO')