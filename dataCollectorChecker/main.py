import os,sys
root = os.getcwd()
os.chdir(root+"/../")
sys.path.append(os.getcwd())
os.chdir(root)
from csvToXmlDataCollector.appDXml import *

print("Let's start, Bakayaro Konoyaro!")