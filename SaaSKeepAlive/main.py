#!-*- coding: utf-8 -*-

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

def sendMessage(msg):
    count = 0
    while count < 5:
        try:
            msgBot.sendMessage(msg)
            logs.write('Mensagem enviada!','DEBUG')
            break
        except Exception as e:
            logs.write('Não foi possível enviar mensagem para o telegram!', 'DEBUG')
            count += 1
            time.sleep(2)
            continue

iniPath = getChecked(1, 'appd_config.ini')
sleepSecs =  int(getChecked(2, 1)) * 60
outTerminal = toBool(getChecked(3, 'False'))
logName = 'main'
logs = logger(iniPath,logName,outTerminal)
print("Logging to "+logName+".log")
ctl = controller(iniPath,logs)
msgBot = telegramApi.telegramApi(iniPath)
xmlApps = xmlElements('applications')

while True:
    logs.clear()
    appResponse = None
    try:
        appResponse = ctl.requestController(ctl.getUrl('applications'))
    except Exception as e:
        msg = 'Falha na comunicação com a Controller. Verifique se o AppDynamics está no ar!\nAcionar equipe de Telemetria.'
        logs.write(msg,'INFO')
        sendMessage(msg)
        appResponse = None

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
                try:
                    logs.write('Getting app infos','DEBUG')
                    appXml = ctl.getAppResponse(app).text
                    xmlApps = xmlElements(app)
                    xmlApps.setRootFromStr(appXml)
                    metricValues = xmlApps.getElementsByTag('metricValues')
                    for el in metricValues:
                        logs.write('Getting node info','DEBUG')
                        totalNodes += 1
                        metric = xmlApps.getElementByTag(el,'metric-value')
                        if metric != None:
                            totalAvailCount += int(xmlApps.getElementByTag(metric,'count').text)
                        else:
                            logs.write('15 min unavailable node for app '+app,'DEBUG')
                except Exception as e:
                    msg = 'Não foi possível processar a application '+app
                    logs.write(msg,'INFO')

            logs.write('All apps processed, processing data','DEBUG')
            totalAvailExpected = totalNodes * 15
            percentAvail = (totalAvailCount * 100) / totalAvailExpected
            percentError = int(ctl.config['DEFAULT']['controller.availability.percent.error'])
            msg = ''
            if percentAvail > percentError:
                msg = 'TotalNodes: '+str(totalNodes)+' | Availability Expected: '+str(totalAvailExpected)+' | Availability: '+str(totalAvailCount)+' | Percent: '+str(percentAvail)+'%'
            else:
                msg = 'Apenas '+str(percentAvail)+'% de nodes disponíveis. Verifique se o AppDynamics está no ar!\nAcionar equipe de Telemetria.'
                sendMessage(msg)
            logs.write(msg,'INFO')
            logs.write('Finished processing!','INFO')
        else:
            msg = 'Nenhuma app disponível, verifique a disponibilidade do controller!'
            logs.write(msg)
            sendMessage(msg)
        time.sleep(sleepSecs)