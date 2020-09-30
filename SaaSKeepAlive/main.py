#Relative import path fix
from importfix import importfix
importfix.setImportPathRoot("../")

#Imports
from csvToXmlDataCollector.appDXml.xmlGenerator import xmlElements
from SaaSKeepAlive.controller import controller
from SaaSKeepAlive.customLogs import logger
from telegramApi import telegramApi
import time,sys

def toBool(s):
    return s.lower() in ['true', '1', 't', 'y', 'yes']

def getChecked(argI,std):
    if len(sys.argv) >= (argI + 1):
        return sys.argv[argI]
    else:
        return std

iniPath = getChecked(1, 'appd_config.ini')
sleepSecs =  int(getChecked(2, 3)) * 60
outTerminal = toBool(getChecked(3, 'False'))
logName = 'main'
logs = logger(iniPath,logName,outTerminal)
print("Logging to "+logName+".log")
ctl = controller(iniPath,logs)
msgBot = telegramApi.telegramApi(iniPath)
xmlApps = xmlElements('applications')

while True:
    appResponse = ctl.requestController(ctl.getUrl('applications'))
    logs.clear()
    if appResponse == None:
        time.sleep(sleepSecs)
        continue
    else:
        applicationsXml = appResponse.text
        xmlApps.setRootFromStr(applicationsXml)
        appNames = [name.text for name in xmlApps.getElementsByTag('name')]
        if len(appNames) > 0:
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
            percentError = int(ctl.config['DEFAULT']['controller.availability.percent.error'])
            msg = ''
            if percentAvail > percentError:
                msg = 'TotalNodes: '+str(totalNodes)+' | Availability Expected: '+str(totalAvailExpected)+' | Availability: '+str(totalAvailCount)+' | Percent: '+str(percentAvail)+'%'
            else:
                msg = 'Apenas '+str(percentAvail)+'% de nodes disponíveis.\nPossível falha no controller!'
                msgBot.sendMessage(msg)
            logs.write(msg,'INFO')
            logs.write('Finished processing!','INFO')
        else:
            logs.write('Nenhuma app disponível')
        time.sleep(sleepSecs)