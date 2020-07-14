import csv
import os

class csvReader(object):
	def __init__(self,filesRoot,csvFileName,delimiterChar):
		csvFilePath = filesRoot+"/templates/"+csvFileName
		self.csv = csvFilePath
		self.delimiterChar = delimiterChar
	
	def getCsvRows(self):
		with open(self.csv) as csvfile:
		    csvRows = csv.reader(csvfile, delimiter=self.delimiterChar)
		    rows = []
		    for row in csvRows:
		    	rows.append(row)
		return rows

	def getRowsWithColumnValue(self,columnIndex,columnValue):
		csvRows = self.getCsvRows()
		validRows = []
		for row in csvRows:
			if row[columnIndex] == columnValue:
				validRows.append(row)
		return validRows

	def getRowsDistinctColumn(self,columnIndex):
		csvRows = self.getCsvRows()
		returnRows = {}
		for row in csvRows:
			if row[columnIndex] in returnRows:
				returnRows[row[columnIndex]].append(row)
			else:
				returnRows.update({row[columnIndex]:[row]})
		return returnRows