#Relative import path fix
from importfix import importfix
importfix.setImportPathRoot("../")

#Package imports
import requests, os, configparser

class controller():
    def __init__(self,pathToConfigFile,loggerObj):
        self.config = configparser.ConfigParser()
        self.logs = loggerObj
        self.__ctlHost = ''
        self.__ctlHttpProtocol = 'http'
        self.__ctlAccount = ''
        self.__ctlUserName = ''
        self.__ctlUserPss = ''
        self.__apiUrls = {}
        self.setConfig(pathToConfigFile)
        self.setControllerConfig()

    def setConfig(self,pathToConfigFile):
        if os.path.exists(pathToConfigFile):
            try:
                self.config.read(pathToConfigFile)
            except Exception as e:
                self.logs.write("Nao foi possivel carregar a configuracao. Exception:\n"+str(e),'DEBUG')
        else:
            self.logs.write("Nao foi possivel carregar a configuracao.\nArquivo nao encontrado!", 'DEBUG')

    def setControllerConfig(self):
        defaultConfig = self.config['DEFAULT']
        self.__ctlHost = defaultConfig['controller.host']
        if defaultConfig.getboolean('controller.ssl.enabled'):
            self.__ctlHttpProtocol = 'https'
        self.__ctlAccount = defaultConfig['controller.account.name']
        self.__ctlUserName = defaultConfig['controller.user.name']
        self.__ctlUserPss = defaultConfig['controller.user.password']
        self.__apiUrls['applications'] = self.__ctlHttpProtocol+'://'+self.__ctlHost+'/controller/rest/applications'
        self.__apiUrls['genericAppAvail'] = self.__apiUrls['applications']+'/GENERICAPP/metric-data?metric-path=Application%20Infrastructure%20Performance%7C*%7CIndividual%20Nodes%7C*%7CAgent%7CApp%7CAvailability&time-range-type=BEFORE_NOW&duration-in-mins=15'

    def getUrl(self,key):
        return self.__apiUrls[key]

    def requestController(self,url):
        try:
            return requests.get(url, auth=(self.__ctlUserName+'@'+self.__ctlAccount, self.__ctlUserPss))
        except Exception as e:
            self.logs.write('Unable to get controller info.\n'+str(e),'DEBUG')
            raise

    def getAppResponse(self,appName):
        url = self.__apiUrls['genericAppAvail'].replace('GENERICAPP',appName)
        try:
            return self.requestController(url)
        except Exception as e:
            raise