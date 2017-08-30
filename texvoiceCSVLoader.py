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

		with open(self.args.inputFile, 'rb') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')
			for entry in reader:
				description = self.get(entry, 'task.description')
				duration = self.get(entry, 'task.duration')
				wage = float(self.get(entry, 'task.wage'))
				vat = float(self.get(entry, 'task.vatPercentage'))
				self.data.addTask(idata.Task(description, duration, wage, vat))
				
		self.applyArgs()
		return self.data
		
	def loadConfig(self, path):
		with open(path, 'rb') as configFile:
			line = configFile.readline()
			while line:
				self.parseConfigLine(line)
				line = configFile.readline()
				
	def parseConfigLine(self, line):
		def chainedFunctions(value, funcs):
			result = value
			for func in funcs:
				result = FUNCTIONS[func.upper()](result)
			return result
			
			
		FUNCTIONS = {
			'FACTOR2PERCENTAGE' : lambda x: (float(x)-1) * 100,
			'TIMESTAMP' : lambda x: idata.Task.parseDuration(x),
			'DECIMALCOMMA' : lambda x: x.replace(',', '.'),
			'DECIMALCOMMA@FACTOR2PERCENTAGE' : lambda x: FUNCTIONS['FACTOR2PERCENTAGE'](FUNCTIONS['DECIMALCOMMA'](x))
		}
		line = line[0:-1]	# Remove trailing \n
		if len(line) is 0 or line.startswith('#'):
			return
		
		if not ': ' in line:
			raise ValueError("malformed line '%s'" % line)
			
		(key, value) = line.split(': ', 1)
		key = key[1:-1]
		function = None
		
		if '\'@' in value:
			(value, func) = value.split('\'@', 1)
			if '@' in func: # Chained functions
				funcs = func.split('@')
				function = lambda x: chainedFunctions(x, funcs)
			else:
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
