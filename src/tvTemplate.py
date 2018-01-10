import copy
import os, shutil
import zipfile


class Template:
	def __init__(self, templateFile):
		if not zipfile.is_zipfile(templateFile):
			raise Exception(templateFile + ' is not a .zip file')
			
		self.templateFile = templateFile
		
		with zipfile.ZipFile(templateFile, "r") as zf:
			templateTexFile = 'template.tex'
			
			if not templateTexFile in zf.namelist():
				raise Exception('Malformed template')
			with zf.open(templateTexFile) as texFile:
				self.tex = texFile.read().decode('UTF-8')
		self.multiTable = self._buildMultiTable()
		
	def _buildMultiTable(self):
		'''
		Get the multiTable from the template
		'''
		multiTable = []
		finger = 0
		while True:
			(start, end) = self._findSection('texvoicePage', beg=finger)
			if start[0] is -1:
				break
			else:
				# Leave the argument in place if it exists
				if self.tex[start[0]+start[1]] == '[':
					idx = self.tex.find(']', start[0]+start[1]+1)
					if idx is -1:
						raise Exception('Unmatched brackets')
					start = (start[0], idx - start[0] + 1)
				
				multiTable.append(self.tex[start[0]+start[1]:end[0]])
				self.tex = self.tex[:start[0]+start[1]] + self.tex[end[0]:]
				finger = start[0] + start[1]	# Do not use end here as this is in the moved indices
		return multiTable

	def export(self, location):
		'''
		Export the template to the given location, so that it can be compiled.
		Make sure the given folder is empty, otherwise things could break.
		'''
		with open(location + 'result.tex', 'w') as f:
			f.write(self.tex)
			
		# Extract the include folder
		includeFolder = 'include/'
		with zipfile.ZipFile(self.templateFile, "r") as zf:
			for file in zf.namelist():
				if file.startswith(includeFolder) and file != includeFolder:
					fileName = file[len(includeFolder):]
					zf.extract(file, location)
					os.rename(location + file, location + file[len(includeFolder):])
		
		# Remove the include folder if it exists
		if os.path.isdir(location + includeFolder):
			shutil.rmtree(location + includeFolder)
				
	
	def applyListings(self, data, applyMultiTable=True, tex=None):
		'''
		Apply all listings.
		'''
		if tex is None:
			tex = self.tex
			
		while True:
			(start, end) = self._findSection('texvoiceListing', tex=tex)
			if start[0] is -1:
				break
			data, tex = self._applyListing(start, end, data, tex)
		
		if applyMultiTable:
			self.tex = tex
			self._applyMultiTable(data)
		return data, tex
				
	def _applyMultiTable(self, data):
		'''
		Apply all the multiTables
		'''
		for page in self.multiTable:
			res = ''
			dataCopy = copy.deepcopy(data)	# There is probably a better way to do this
			
			# Check if we need to prefix anything, and if so apply
			fix = ''
			(start, end) = self._findSection('texvoicePage')
			idx = start[0]+start[1]
			if self.tex[idx] == '[':
				fix = self.tex[idx + 1: self.tex.find(']', idx)] + '\n'
				
			# Apply all listings until there is no more data
			while True:
				(data, tex) = self.applyListings(data, applyMultiTable=False, tex=page)
				
				# If nothing is applied
				if(dataCopy == data):
					break
				else:
					dataCopy = copy.deepcopy(data)
				
				res += fix + tex
				
				# Nothing more can be applied
				if all(key == 'accumulated' or len(data[key]['data']) is 0 for key in data):
					break
				
			self.tex = self.tex[:start[0]] + res + self.tex[end[0]+end[1]:]
			
	def _findSection(self, name, beg=0, tex=None):
		'''
		Find a section with a given name in the input.
		When a starting point is given only returns a section after that point
		'''
		if tex is None:
			tex = self.tex
		startStr = '\\begin{%s}' % name
		endStr = '\\end{%s}' % name
		
		start = tex.find(startStr, beg)
		if start is -1:
			return ((-1, len(startStr)), (-1, len(endStr)))
		end = tex.find(endStr, start)
		if end is -1:
			raise Exception('Cannot find closing tag for %s' % name)
		return ((start, len(startStr)), (end, len(endStr)))

	def _applyListing(self, start, end, data, tex):
		'''
		Apply as much of the data as is possible in the given range.
		Returns the result and the data that couldn't be applied.
		'''
		res = ''
		strt = start[0] + start[1]
		if tex[strt] == '[':
			nd = tex.find(']', strt)
			runs = int(tex[strt+1:nd])
			tex = tex[:strt] + (nd+1 - strt) * ' ' + tex[nd+1:]	# Overwrite with spaces to not break the start and end indices
		else:
			runs = -1
			
		while runs is -1 or runs > 0:
			runs = max(-1, runs-1)
			(didApplyGroup, tmp, totals) = (False, tex[ (start[0] + start[1]) : (end[0]) ], {'subtotal':0, 'vat':0})
			# For each group
			for group in data:
				if group == 'accumulated':
					continue
				(didApply, tmp, totals) = self._applyGroup(data[group], group, totals, tex=tmp)
				didApplyGroup = didApplyGroup or didApply
			
			# If you did apply anythng store it otherwise we are done
			if didApplyGroup:
				# Apply listing accumulates
				subtotal = totals['subtotal']
				vat = totals['vat']
				
				tmp = self.applyField('subtotal', '€%.2f' % subtotal, tmp)
				tmp = self.applyField('total', '€%.2f' % (subtotal + vat), tmp)
				tmp = self.applyField('vatPercentage', '%.2f\\%%' % ((vat/subtotal) * 100) if not (vat == 0) else '0\\%', tmp)
				tmp = self.applyField('vat', '€%.2f' % vat, tmp)
				
				res += tmp
			else:
				break
		
		tex = tex[:start[0]] + res + tex[end[0] + end[1]:]
		return data, tex
		
	def applyField(self, key, value, tex):
		'''
		Apply all the fields with the given name to get the given value.
		'''
		FUNCTIONS = {
			'vat': lambda key, val: '%.2f\\%%' % float(val),
			'unitPrice': lambda key, val: '€%.2f' % float(val),
			'unit': lambda key, val: str(val) if not (key == 'duration') else (lambda v: str(int(v)) + ':' + '%02d' % (int((v%1)*60))) (float(val))
		}
		if '(' in key:
			key, func = key.split('(')
			func = func[:-1]
			if func in FUNCTIONS:
				value = FUNCTIONS[func](key, str(value))
		return tex.replace('\\' + key, str(value))
		
	def _applyGroup(self, data, group, totals, tex=None):
		'''
		Apply a single entry for the given group in the template.
		Return True when an entry is applied, False otherwise.
		'''
		def addTotals(totals, data, keys):
			'''
			Add the totals of the given data to the totals dictionary
			'''
			keys = list(map((lambda x: None if not '(' in x else (lambda a, b: b[:-1]) (*x.split('('))), keys))
			if all(e is None for e in keys):
				return totals
				
			units = float(data[keys.index('unit')]) if 'unit' in keys else 1
			subtotal = units * float(data[keys.index('unitPrice')])
			vat = subtotal * (float(data[keys.index('vat')]) / 100)
			
			totals['subtotal'] += subtotal
			totals['vat'] += vat
			
			return totals
			
		if tex is None:
			tex = self.tex
		finger = 0		
		row = None
		
		# Do not pop the data when it is not needed
		if (not len(data['data']) is 0) and (lambda x, y: not x[0] is -1)(*self._findSection(group, tex=tex)):
			row = data['data'].pop(0)
			totals = addTotals(totals, row, data['keys'])
		
		# Change all the groups
		changed = False
		while True:
			(start, end) = self._findSection(group, tex=tex, beg=finger)
			finger = end[0] + end[1]
			
			# All groups done
			if start[0] is -1:
				break
			
			# Remove unneeded group
			if not row:
				tex = tex[:start[0]] + tex[end[0]+end[1]:]
				continue
			
			changed = True
			result = tex[start[0]+start[1]:end[0]]
			
			for key in reversed(sorted(data['keys'])):
				value = row[data['keys'].index(key)]
				result = self.applyField(key, value, result)
			tex = tex[:start[0]] + result + tex[end[0]+end[1]:]
		
		return (changed, tex, totals)

	def applyGlobalAccumulatives(self, data):
		'''
		Apply the global data accumulations to the file.
		'''
		groupData = data['groups']
		for group in groupData:
			self.tex = self._applyGroup(groupData[group], group, {})[1]
		
		globalData = data['global']
		for field in reversed(sorted(globalData['keys'])):
			value = globalData['data'][0][globalData['keys'].index(field)]
			self.tex = self.applyField(field, value, self.tex)

	def applyGlobalFields(self, options):
		'''
		Apply all the options to the input.
		'''
		for field, value in options.items():
			self.tex = self.applyField(field, str(value), self.tex)
