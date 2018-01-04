class Template:
	def __init__(self, templateFile):
		self.templateFile = templateFile
		self._tex = None
		self._version = None
		self._requiredFields = []
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

	def applyListings(self, data):
		while True:
			(start, end) = self._findSection('texvoiceListing')
			if start[0] is -1:
				break
			data = self._applyListing(start, end, data)
			
	def applyGlobals(self, data):
		pass
		
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
		return tex.replace('\\' + key, value)
		
	def _applyGroup(self, data, group, tex=None):
		'''
		Apply a single entry for the given group in the template.
		Return True when an entry is applied, False otherwise.
		'''
		if tex is None:
			tex = self.tex
		(start, end) = self._findSection(group, tex=tex)
		if start[0] is -1:
			return (False, tex)
			
		if len(data['data']) is 0:
			return (False, tex[:start[0]] + tex[end[0]+end[1]:])
			
		result = tex[start[0]+start[1]:end[0]]
		row = data['data'].pop(0)
		for index, key in enumerate(data['keys']):
			value = row[index]
			result = self.applyField(key, str(value), result)
		
		return (True, tex[:start[0]] + result + tex[end[0]+end[1]:])

	def applyGlobal(self, data, template=None):
		'''
		Apply a the global data in the template.
		Return True when data is applied, False otherwise.
		'''
		if template is None:
			template = self.tex
		for group in data:
			# TODO: Apply the accumulative data for each group
			# ApplyGroup(data[group], group, start, end, template)
			pass
		# TODO: Apply the global accumulatives
		return False

	def applyOptions(self, options):
		'''
		Apply all the options to the input.
		'''
		pass
