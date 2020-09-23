from importer import importerFixer
importerFixer.setImportPathRoot("../")
from csvToXmlDataCollector.appDXml.xmlGenerator import xmlElements

import requests, os
from SaaSKeepAlive.controller import controller

ctl = controller('./appd_config.ini')

xmlApps = xmlElements(os.getcwd(),'applications')

resp = ctl.requestController(ctl.getUrl('applications'))

xmlApps.setRootFromStr(resp.text)
appNames = ['Agenda'] #[name.text for name in xmlApps.getElementsByTag('name')] #['dev-namespace']
appsXmls = []
for app in appNames:
    appXml = ctl.getAppResponse(app).text
    appsXmls.append(appXml)
    xmlApps = xmlElements(os.getcwd(),app)
    xmlApps.setRootFromStr(appXml)
    print('\nFor APP: '+app)
    metricValues = xmlApps.getElementsByTag('metricValues')
    metricNames = []
    for el in metricValues:
        metric = xmlApps.getElementByTag(el,'metric-value')
        if metric != None:
            value = xmlApps.getElementByTag(metric,'value')
            print(value.tag+': '+value.text)
        else:
            print('EMPTY: '+el.tag+': '+str(len(list(el))))
    #print(str(list(metricNames))+'\n')
    xmlApps.writeTree()