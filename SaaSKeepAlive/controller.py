#Ref for local imports
from importer import importerFixer
importerFixer.setImportPathRoot("../")

#Imports
import requests, os, configparser
from csvToXmlDataCollector.appDXml.xmlGenerator import xmlElements

class controller():
	def __init__(self,pathToConfigFile):
        self.config = configparser.ConfigParser()
        self.__ctlHost = ''
        self.__ctlHttpProtocol = 'http'
        self.__ctlAccount = ''
        self.__ctlUserName = ''
        self.__ctlUserPss = ''
        self.__apiUrls = {}

    def setConfig(self,pathToConfigFile):
        if os.path.exists(pathToConfigFile):
            try:
                self.config.read(pathToConfigFile)
            except Exception as e:
                print("Nao foi possivel carregar a configuracao. Exception:\n"+str(e))
        else:
            print("Nao foi possivel carregar a configuracao.\nArquivo nao encontrado!")
    
    def setControllerConfig(self):
        defaultConfig = self.config['DEFAULT']
        self.__ctlHost = defaultConfig['controller.host']
        if defaultConfig.getboolean('controller.ssl.enabled'):
            self.__ctlHttpProtocol = 'https'
        #self.__ctlHost = defaultConfig['controller.host']
        #self.__ctlHost = defaultConfig['controller.host']
        #self.__ctlHost = defaultConfig['controller.host']
        #{'applications':'HTTP://URL_CONTROLLER/controller/rest/applications', 'genericAppAvail':'https://URL_CONTROLLER/controller/rest/applications/GENERICAPP/metric-data?metric-path=Application%20Infrastructure%20Performance%7C*%7CIndividual%20Nodes%7C*%7CAgent%7CApp%7CAvailability&time-range-type=BEFORE_NOW&duration-in-mins=15'}