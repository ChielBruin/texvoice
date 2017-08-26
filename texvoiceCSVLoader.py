# coding: UTF-8
import csv

import texvoiceDataLoader
import inputData as idata

class TexvoiceCSVLoader(texvoiceDataLoader.TexvoiceDataLoader):
	config = {}
	
	def load(self, dataFile, template, output, args):
		self.data = idata.InputData(template, output)
		self.loadConfig('csvConfigs/Timesheet_NL.conf')
		print self.config
		with open(dataFile, 'rb') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')
			for entry in reader:
				description = self.get(entry, 'task.description')
				duration = self.get(entry, 'task.duration')
				wage = float(self.get(entry, 'task.wage'))
				self.data.addTask(idata.Task(description, duration, wage))
				
		self.applyArgs(args)
		return self.data
		
	def loadConfig(self, path):
		with open(path, 'rb') as configFile:
			line = configFile.readline()
			while line:
				self.parseConfigLine(line)
				line = configFile.readline()
				
			print(self.config)
				
	def parseConfigLine(self, line):
		FUNCTIONS = {
			'FACTOR2PERCENTAGE' : lambda x: int((float(x)-1) * 100),
			'TIMESTAMP' : lambda x: idata.Task.parseDuration(x),
			'DECIMALCOMMA' : lambda x: x.replace(',', '.')
		}
		line = line[0:-1]	# Remove trailing \n
		if len(line) is 0 or line.startswith('#'):
			return
		
		if not ': ' in line:
			raise ValueError("malformed line '%s'" % line)
			
		(key, value) = line.split(': ', 1)
		key = key[1:-1]
		function = None
		
		if "@" in value:
			(value, func) = value.rsplit('@', 1)
			function = FUNCTIONS[func.upper()]
			
		if value is 'None':
			value = None
			
		self.config[key] = (value, function)
		
	def get(self, data, key):
		(value, func) = self.config[key]
		
		if value is None:
			# Load from argparser
			pass
		else:
			result = data[value]
			if func:
				result = func(result)
		return result

	def applyArgs(self, args):
		self.data.invoice.id = '02'
		self.data.project.id = 'MTIS'
		self.data.project.client = 'M-TIS'
		self.data.project.description = ''
