#!/usr/bin/env python

class Template:
	def __init__(self, templateFile):
		self.templateFile = templateFile
		self._tex = None
		self._version = None
		self._requiredFields = None
		self._data = {}
			
	@property
	def tex(self):
		'''
		Get the actual template file and cache the result
		'''
		if self._tex is None:
			with open(self.templateFile, 'r') as f:
				self._tex = f.read()
		return self._tex
		
	@property
	def requiredFields(self):
		'''
		Get the required fields and cache the result
		'''
		if self._requiredFields is None:
			self._requiredFields = [
				('invoiceID', 'The ID of this invoice'),
				('projectID', 'The ID of this project')
			]
		return self._requiredFields

	def applyListings(self, data):
		'''
		Apply all listings.
		'''
		while True:
			(start, end) = self._findSection('texvoiceListing')
			if start[0] is -1:
				break
			data = self._applyListing(start, end, data)
		
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

	def _applyListing(self, start, end, data):
		'''
		Apply as much of the data as is possible in the given range.
		Returns the result and the data that couldn't be applied.
		'''
		res = ''
		while True:
			(didApplyGroup, tmp) = (False, self.tex[ (start[0] + start[1]) : (end[0]) ])
			# For each group
			for group in data:
				if group == 'accumulated':
					continue
				(didApply, tmp) = self._applyGroup(data[group], group, tex=tmp)
				didApplyGroup = didApplyGroup or didApply
			
			# Global accumulates
			didApplyGlobal = False
			#(didApplyGlobal, tmp) = self._applyGlobal(data['global'], tex=tmp)
			
			# If you did apply anythng store it otherwise we are done
			if didApplyGlobal or didApplyGroup:
				 res += tmp
			else:
				break
		
		self._tex = self._tex[:start[0]] + res + self._tex[end[0] + end[1]:]
		return data
		
	def applyField(self, key, value, tex):
		'''
		Apply all the fields with the given name to get the given value.
		'''
		FUNCTIONS = {
			'vat': lambda key, val: str(val)+'\\%',
			'unitPrice': lambda key, val: '%.2f'%float(val),
			'unit': lambda key, val: str(val) if not (key == 'duration') else (lambda v: str(int(v)) + ':' + '%02d' % (int((v%1)*60))) (float(val))
		}
		if '(' in key:
			key, func = key.split('(')
			func = func[:-1]
			if func in FUNCTIONS:
				value = FUNCTIONS[func](key, str(value))
		return tex.replace('\\' + key, str(value))
		
	def _applyGroup(self, data, group, tex=None):
		'''
		Apply a single entry for the given group in the template.
		Return True when an entry is applied, False otherwise.
		'''
		if tex is None:
			tex = self.tex
		finger = 0		
		row = None
		
		#print(group, data, self._findSection(group, tex=tex))
		# Do not pop the data when it is not needed
		if (not len(data['data']) is 0) and (lambda x, y: not x[0] is -1)(*self._findSection(group, tex=tex)):
			row = data['data'].pop(0)
		
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
		
		return (changed, tex)

	def applyGlobalAccumulatives(self, data):
		'''
		Apply the global data accumulations to the file.
		'''
		groupData = data['groups']
		for group in groupData:
			self._tex = self._applyGroup(groupData[group], group)[1]
		
		globalData = data['global']
		for field in reversed(sorted(globalData['keys'])):
			value = globalData['data'][0][globalData['keys'].index(field)]
			self._tex = self.applyField(field, value, self._tex)

	def applyGlobalFields(self, options):
		'''
		Apply all the options to the input.
		'''
		for field, value in options.items():
			self._tex = self.applyField(field, str(value), self._tex)
