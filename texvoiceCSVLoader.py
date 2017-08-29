# coding: UTF-8
import csv, argparse

import texvoiceDataLoader
import inputData as idata

class TexvoiceCSVLoader(texvoiceDataLoader.TexvoiceDataLoader):
	config = {}
	def __init__(self):
		super(TexvoiceCSVLoader, self).__init__()
		self.parser.add_argument('config', choices=['Timesheet_NL'], help="Specify the CSV config file")

	def load(self, args):
		self.args = self.parser.parse_args(args)
		self.data = idata.InputData(self.args.template, self.args.outputFile, self.args.keepSource)
		self.loadConfig('csvConfigs/Timesheet_NL.conf')
		print self.config
		with open(self.args.inputFile, 'rb') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')
			for entry in reader:
				description = self.get(entry, 'task.description')
				duration = self.get(entry, 'task.duration')
				wage = float(self.get(entry, 'task.wage'))
				self.data.addTask(idata.Task(description, duration, wage))
				
		self.applyArgs()
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
		
		# Remove the quotes around the values
		value = ''.join(value.replace('\'', '', 1).rsplit('\'', 1))
		self.config[key] = (value, function)
		
	def get(self, data, key):
		(value, func) = self.config[key]
		
		if value is None:
			if key is 'task.vatPercentage':
				result = self.args.vat
			else:
				raise ValueError('No value or data column could be found for ' + key)
		else:
			result = data[value]
			if func:
				result = func(result)
		return result
