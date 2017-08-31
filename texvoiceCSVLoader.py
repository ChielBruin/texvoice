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
		self.data = idata.InputData(self.args.template, self.args.keepSource)
		self.loadConfig('csvConfigs/Timesheet_NL.conf')

		with open(self.args.inputFile, 'rb') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')
			for entry in reader:
				travel = self.getTravel(entry)
				if bool(self.get(entry, 'task.travel.exclusive')) and travel:
					task = None
					expenses = None
				else:	
					task = self.getTask(entry)
					expenses = self.getExpenses(entry)
				self.data.addEntry(task, expenses, travel)

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
				result = parseFunc(func)(result)
			return result
			
		def parseFunc(func):
			arg = None
			if '{' in func:
				(func, arg) = ''.join(func.rsplit('}', 1)).split('{')
			return lambda x: FUNCTIONS[func.upper()](x, arg)
			
		FUNCTIONS = {
			'FACTOR2PERCENTAGE' : lambda x, arg: (float(x)-1) * 100,	# Make a percentage from a factor (multiplier)
			'TIMESTAMP' : lambda x, arg: idata.Task.parseDuration(x),	# Parse a duration timestamp to a float
			'DECIMALCOMMA' : lambda x, arg: x.replace(',', '.'),		# Replace the comma to a dot in the decimal notation
			'DEFAULT' : lambda x, arg: arg if x is '' else x,			# When empty insert the default value
			'OVERRIDE' : lambda x, arg: arg,							# Override any content with the argument
			'EMPTY' : lambda x, arg: '' if x is arg else x				# If equal to the argument make it empty
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
				function = parseFunc(func)
			
		if value is 'None':
			value = None
		
		# Remove the quotes around the values
		value = ''.join(value.replace('\'', '', 1).rsplit('\'', 1))
		self.config[key] = (value, function)
		
	def get(self, data, key):
		(value, func) = self.config[key]
		
		if value is '' and func:
			return func(value)
			
		if value is None:
			if key is 'task.vatPercentage':
				result = self.args.vat
			else:
				raise ValueError('No value or data column could be found for ' + key)
		else:
			result = data[value]
			if func:
				result = func(result)
			if not result is '':
				return result
			else:
				return None

	def getTask(self, entry):
		description = self.get(entry, 'task.description')
		duration = self.get(entry, 'task.duration')
		wage = float(self.get(entry, 'task.wage'))
		vat = float(self.get(entry, 'task.vatPercentage'))

		return idata.Task(description, duration, wage, vat)
		
	def getExpenses(self, entry):
		description = self.get(entry, 'task.expenses.description')
		price = float(self.get(entry, 'task.expenses.price'))
		vat = float(self.get(entry, 'task.expenses.vatPercentage'))
		
		if description:
			return idata.Expenses(description, price, vat)
		else:
			return None
		
	def getTravel(self, entry):
		description = self.get(entry, 'task.travel.description')
		price = self.get(entry, 'task.travel.price')
		vat = self.get(entry, 'task.travel.vatPercentage')
		fromLocation = self.get(entry, 'task.travel.from')
		toLocation = self.get(entry, 'task.travel.to')
		distance = self.get(entry, 'task.travel.distance')

		print distance
		
		if distance:
			return idata.Travel(description, float(price), float(vat), fromLocation, toLocation, float(distance))
		else:
			return None
