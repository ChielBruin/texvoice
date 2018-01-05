from __future__ import division

import texcaller
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
	
	return template.tex

def compile(latex, options):
	'''
	Compile the given .tex input to PDF and store the result in the given file location
	'''
	pdf, info = texcaller.convert(latex, 'LaTeX', 'PDF', 5)

	with open(options['resultFile'], 'w') as f:
		f.write(pdf)
	
	return (not (pdf is []), info)
	
def checkTemplateVersion(version):
	'''
	Check if the given template version is compatible with the compiler.
	'''
	return version in [2, 3]
	
def generateAccumulatives(data):
	'''
	Generate the totals from the data.
	'''
	acc = {
		'groups': {},
		'global': {}
	}
	
	for group in data:
		keys = map((lambda x: None if not '(' in x else (lambda a, b: b[:-1]) (*x.split('('))), data[group]['keys'])
		
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
		totalSubtotal = totalVat = totalTotal = 0
		
		# Add totals to each row and add to global totals
		for row in data[group]['data']:
			unit = float(row[unitIdx]) if unitIdx >= 0 else 1	# Default to 1 unit when none given
			unitPrice = float(row[unitPriceIdx])
			vatPercentage = float(row[vatIdx])
			
			subtotal = unit * unitPrice
			vat = subtotal * (vatPercentage/100)
			total = subtotal + vat
			
			row.extend([str(subtotal), str(vat), str(total)])
			
			totalUnits += unit
			
			totalSubtotal += subtotal
			totalVat += vat
			totalTotal += total
		
		acc['groups'][group] = {'keys': ['subtotal', 'vat', 'total'], 'data': [[str(totalSubtotal), str(totalVat), str(totalTotal)]]}
		
		accData = acc['groups'][group]
		keys = data[group]['keys']
		
		accData['keys'].extend([
			keys[unitPriceIdx].split('(')[0], 
			keys[unitIdx].split('(')[0],
			keys[vatIdx].split('(')[0]
		])
		accData['data'][0].extend([
			str(totalSubtotal / totalUnits) if not (totalUnits == 0) else '0',
			str(totalUnits),
			str((totalVat/totalSubtotal) * 100) if not (totalVat == 0) else '0'
		])
	data['accumulated'] = acc
