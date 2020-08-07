import csv
import os

class csvReader(object):
	def __init__(self,filesRoot,csvFileName,delimiterChar):
		csvFilePath = filesRoot+"/templates/"+csvFileName
		self.csv = csvFilePath
		self.delimiterChar = delimiterChar

	def trimRows(self,rows):
		for count in range(0,len(rows)):
			for c in range(0,len(rows[count])):
				column = rows[count][c]
				newValue = column.strip()
				rows[count][c] = newValue
		return rows
	
	def getCsvRows(self):
		rows = []
		try:
			with open(self.csv, encoding='utf-8-sig') as csvfile:
			    csvRows = csv.reader(csvfile, delimiter=self.delimiterChar)
			    for row in csvRows:
			    	rows.append(row)
		except Exception as e:
			print("Exception"+str(e)+", ao abrir o arquivo "+self.csv)
		else:
			pass
		finally:
			return self.trimRows(rows)

	def getRowsWithColumnValue(self,columnIndex,columnValue):
		csvRows = self.getCsvRows()
		validRows = []
		for row in csvRows:
			try:
				if row[columnIndex] == columnValue:
					validRows.append(row)
			except Exception as e:
				print("Exception"+str(e)+", ao buscar a posição "+columnIndex+" da linha do csv.")
			else:
				pass
			finally:
				return validRows

	def getRowsDistinctColumn(self,columnIndex):
		csvRows = self.getCsvRows()
		returnRows = {}
		for row in csvRows:
			colunaChave = row[columnIndex].strip()
			if row[columnIndex] in returnRows:
				returnRows[row[columnIndex]].append(row)
			else:
				returnRows.update({row[columnIndex]:[row]})
		return returnRows
