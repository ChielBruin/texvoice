import csv


def load(rawData, options):
	'''
	Load a CSV file with the given CSV options
	'''
	if not "configFile" in options:
		raise Exception("Please specify the 'configFile' field")
		
	config = parseConfig(options["configFile"])
	data = buildInitialData(config)
	
	reader = csv.DictReader(rawData, delimiter=',')
	for row in reader:
		parseRow(row, data, config)
	return data

def buildInitialData(config):
	'''
	Build the initial structure of the data object following the config
	'''
	data = {}
	for _, entry in config.items():
		for (field, _) in entry:
			group, name = field.split('.', 1)
			
			if '!' in group:
				group = group[1:]

			if group in data:
				data[group]['keys'].append(name)
				data[group]['keys'].sort()
			else:
				data[group] = {'keys': [name], 'data': []}
			
	return data
	
def parseConfig(configFile):
	'''
	Parse the given config file.
	The result is a list of CSV collums and a pair of the stored data and an optional function to apply before storing
	'''
	config = {}
	with open(configFile, 'r') as cf:
		line = cf.readline()
		while line:
			res = parseConfigLine(line)
			if res:
				(col, val) = res
				if col in config:
					config[col].append(val)
				else:
					config[col] = [val]
			line = cf.readline()
	return config

def parseRow(row, data, config):
	'''
	Parse a single row of the CSV file and put it in the data object.
	'''
	newData = {}
	incomplete = []
	for tag in row:
		# Skip data for which we do not know what to do
		if not (tag in config):
			continue
		for (fieldDesc, func) in config[tag]:
			group, field = fieldDesc.split('.', 1)
			val = str(func(row[tag]) if func else row[tag])	# Apply function if needed
			
			# If this value is important and missing, remove the group
			if '!' in group:
				group = group[1:]
				if val is '':
					incomplete.append(group)
					break
			
			
			if not (group in newData):
				newData[group] = [(field, val)]
			else:
				newData[group].append((field, val))

	# Remove all incomplete groups
	for group in incomplete:
		newData[group] = []

	# Update the data with the new data
	for group in newData:
		values = newData[group]
		if not values:
			continue
		headers = data[group]['keys']
		new = [None] * len(headers)
		for (field, val) in values:
			new[headers.index(field)] = val
		data[group]['data'].append(new)

def parseConfigLine(line):
	'''
	Parse a single line of the config file.
	'''
	def chainedFunctions(value, funcs):
		result = value
		for func in funcs:
			result = parseFunc(func)(result)
		return result
		
	def parseFunc(func):
		arg = None
		if '{' in func:
			(func, arg) = ''.join(func.rsplit('}', 1)).split('{')
		if not func.upper() in FUNCTIONS:
			raise Exception('Unknown function ' + func)
		return lambda x: FUNCTIONS[func.upper()](x, arg)
		
	FUNCTIONS = {
		'ENDON' : lambda x, arg: x.split(arg)[0],					# Split a string to end on the specified character(s)
		'FACTOR2PERCENTAGE' : lambda x, arg: (float(x)-1) * 100,	# Make a percentage from a factor (multiplier)
		'DECIMALCOMMA' : lambda x, arg: x.replace(',', '.'),		# Replace the comma to a dot in the decimal notation
		'DEFAULT' : lambda x, arg: arg if x is '' else x,			# When empty insert the default value
		'EMPTY' : lambda x, arg: '' if x is arg else x,				# If equal to the argument make it empty
		'TIMESTAMP' : lambda x, arg: 								# Parse a duration timestamp to a float
				(lambda time: float(time[0] + time[1] / float(60)))(list(map(lambda v: int(v), x.split(':'))))
	}
	
	# Pre-checks
	line = line[0:-1]	# Remove trailing \n
	if len(line) is 0 or line.startswith('#'):
		return None
	if not ': ' in line:
		raise ValueError("malformed line '%s'" % line)
		
	(col, key) = line.split(': ', 1)
	
	# Parse functions
	function = None
	if '@' in key:
		(key, func) = key.split('@', 1)
		if '@' in func: # Chained functions
			function = lambda x: chainedFunctions(x, func.split('@'))
		else:
			function = parseFunc(func)
	
	# Remove surrounding brackets and return
	c = (''.join(key.replace('\'', '', 1).rsplit('\'', 1)), function)
	col = ''.join(col.replace('\'', '', 1).rsplit('\'', 1))
	return (col, c)
	
