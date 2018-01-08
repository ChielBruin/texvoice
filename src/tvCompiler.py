import shutil, os, subprocess
import tvTemplate


def loadTemplate(templateFile):
	'''
	Load the specified template file from disk.
	'''
	return tvTemplate.Template(templateFile)
	
def convert(inputData):
	'''
	Convert the template and the data to a .tex file that can be compiled
	'''
	options = inputData['options']
	data = inputData['data']
	generateAccumulatives(data)
	
	template = loadTemplate(options['template'])
	
	template.applyListings(data)
	template.applyGlobalAccumulatives(data['accumulated'])
	template.applyGlobalFields(inputData['global'])
	
	return template

def compile(template, options):
	'''
	Compile the given .tex input to PDF and store the result in the given file location
	'''
	wd = '.tmp'
	
	# Make tmp folder
	if not os.path.exists(wd):
		os.makedirs(wd)
	wd += '/'
	
	# Write the needed files
	template.export(wd)
	
	# Compile to PDF
	result = (False, '')
	try:
		output = subprocess.check_output(['pdflatex', '-interaction=nonstopmode', 'result.tex'], stderr=subprocess.STDOUT, cwd=wd)
		result = (True, output.decode("utf-8"))
	except subprocess.CalledProcessError as e:
		output = e.output.decode("utf-8")
		result = (False, output)
	
	# Get the output files
	files = ['result.pdf']
	if options['keepSource']:
		files.append('result.tex')
		
	for f in files:
		os.rename(wd + f, f)
	
	# Remove the tmp folder
	shutil.rmtree(wd)
	
	return result
	
def checkTemplateVersion(version):
	'''
	Check if the given template version is compatible with the compiler.
	'''
	return version in [2, 3]
	
def priceToString(price):
	'''
	Convert a price to a string representation.
	'''
	return '€%.2f'%price
	
def generateAccumulatives(data):
	'''
	Generate the totals from the data.
	'''
	acc = {
		'groups': {},
		'global': {}
	}
	
	globalSubtotal = globalVat = 0
	
	# Accumulate each group separately
	for group in data:
		keys = list(map((lambda x: None if not '(' in x else (lambda a, b: b[:-1]) (*x.split('('))), data[group]['keys']))
		
		# If nothing should be accumilated, continue
		if all(e is None for e in keys):
			continue
			
		if not ('unitPrice' in keys and 'vat' in keys):
			raise Exception('Malformed accumilative descriptors, both vat and unitPrice must be present')
			
		# Get the data indices
		unitPriceIdx = keys.index('unitPrice')
		if 'unit' in keys:
			unitIdx = keys.index('unit')
		else:
			unitIdx = -1
		vatIdx = keys.index('vat')
		
		# Add the new keys
		data[group]['keys'].extend(['subtotal', 'vat', 'total'])
		
		totalUnits = 0
		totalSubtotal = totalVat = 0
		
		# Add totals to each row and add to global totals
		for row in data[group]['data']:
			unit = float(row[unitIdx]) if unitIdx >= 0 else 1	# Default to 1 unit when none given
			unitPrice = float(row[unitPriceIdx])
			vatPercentage = float(row[vatIdx])
			
			# Calculate local totals and add them to the data
			subtotal = unit * unitPrice
			vat = subtotal * (vatPercentage/100)
			total = subtotal + vat
			
			row.extend([
				priceToString(subtotal), 
				priceToString(vat), 
				priceToString(total)
			])
			
			# Add to the accumilative data
			totalUnits += unit
			totalSubtotal += subtotal
			totalVat += vat
		
		# Add group totals to the data
		acc['groups'][group] = {'keys': ['subtotal', 'vat', 'total'], 'data': [[
			priceToString(totalSubtotal), 
			priceToString(totalVat), 
			priceToString(totalSubtotal + totalVat)
		]]}
		
		accData = acc['groups'][group]
		keys = data[group]['keys']
		
		accData['keys'].extend([
			keys[unitPriceIdx].split('(')[0], 
			keys[unitIdx].split('(')[0],
			keys[vatIdx].split('(')[0]
		])
		accData['data'][0].extend([
			priceToString(totalSubtotal / totalUnits) if not (totalUnits == 0) else '0',
			str(totalUnits),
			'%.2f\\%%' % ((totalVat/totalSubtotal) * 100) if not (totalVat == 0) else '0\\%'
		])
		
		# Add group totals to accumilative totals
		globalSubtotal += totalSubtotal
		globalVat += totalVat
		
	# Add the global totals
	acc['global'] = {'keys': ['subtotal', 'vat', 'vatPercentage', 'total'], 'data': [[
		priceToString(globalSubtotal), 
		priceToString(globalVat), 
		'%.2f\\%%' % ((globalVat/globalSubtotal) * 100) if not (globalVat == 0) else '0\\%', 
		priceToString(globalSubtotal + globalVat)
	]]}
	data['accumulated'] = acc
