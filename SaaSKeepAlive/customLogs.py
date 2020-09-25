#Ref for local imports
from importfix import importfix
importfix.setImportPathRoot("../")

#Package imports
import configparser, os, time

class logger():
    def __init__(self,pathToConfigFile,logname,withPrintIn):
        self.config = configparser.ConfigParser()
        self.setConfig(pathToConfigFile)
        self.logname = logname
        logConfig = self.config['LOGGING']
        self.__logLevel = logConfig['log.level'].upper()
        self.__file = None
        self.__logOpen()
        self.withPrint = withPrintIn
    
    def setConfig(self,pathToConfigFile):
        if os.path.exists(pathToConfigFile):
            try:
                self.config.read(pathToConfigFile)
            except Exception as e:
                print("Nao foi possivel carregar a configuracao. Exception:\n"+str(e))
        else:
            print("Nao foi possivel carregar a configuracao.\nArquivo nao encontrado!")
    
    def getLogLevel(self):
        return self.__logLevel
    
    def __writeFile(self,message):
        self.__logOpen()
        self.__file.write(message+'\n')
        self.__logClose()
    
    def sulfix(self):
        return str(time.asctime()+' | ['+self.getLogLevel()+']: ')
    
    def write(self,logMessage,logLevel):
        if logMessage == '':
            pass
        else:
            fullMessage = str(self.sulfix()+logMessage)
            if self.withPrint:
                print(fullMessage)
            logLevel = logLevel.upper()
            if self.getLogLevel() == logLevel:
                self.__writeFile(fullMessage)
            else:
                if self.getLogLevel() == 'DEBUG':
                    self.__writeFile(fullMessage)
    
    def clear(self):
        self.__logOpen()
        self.__file.truncate(0)
        self.__logClose()
    
    def __logOpen(self):
        if self.__file == None or self.__file.closed:
            self.__file = open(self.logname+".log", "a+")
    
    def __logClose(self):
        if not self.__file == None or not self.__file.closed:
            self.__file.close()