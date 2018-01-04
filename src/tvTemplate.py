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
		listings = self._getListings()
		result = ''
		for (start, end) in listings:
			data = self._applyListing(start, end, data)
			
	def applyGlobals(self, data):
		pass
		
	def _findSection(self, name, beg=0):
		'''
		Find a section with a given name in the input.
		When a starting point is given only returns a section after that point
		'''		
		startStr = '\\begin{%s}' % name
		endStr = '\\end{%s}' % name
		
		start = self.tex.find(startStr, beg)
		if start is -1:
			return ((-1, len(startStr)), (-1, len(endStr)))
		end = self._tex.find(endStr, start)
		if end is -1:
			raise Exception('Cannot find closing tag for %s' % name)
		return ((start, len(startStr)), (end, len(endStr)))
		
	def _getListings(self):
		'''
		Get a list of the positions of all the listings in the input
		'''
		res = []
		finger = 0
		self.tex	# Load if not present
		while (True):
			(start, end) = self._findSection('texvoiceListing', finger)
			if (start[0] is -1):
				return res
			else:
				finger = end[0] + end[1]
				res.append((start, end))

	def _applyListing(self, start, end, data):
		'''
		Apply as much of the data as is possible in the given range.
		Returns the result and the data that couldn't be applied.
		'''
		
		template = self.tex[ (start[0] + start[1]) : (end[0]) ]
		res = ''
		
		while True:
			(didApplyGroup, tmp) = (False, template)
			
			# For each group
			for group in data:
				didApplyGroup = self._applyGroup(data[group], group, start, end)
			
			# Global accumulates
			didApplyGlobal = self._applyGlobal(data['global'], start, end)
			
			# If you did apply anythng store it otherwise we are done 
			if didApplyGlobal or didApplyGroup:
				 res += tmp
			else:
				break
		
		self._tex = self._tex[:start[0]] + res + self._tex[end[0] + end[1]:]
		return data

	def _applyGroup(self, data, group, start, end, template=None):
		'''
		Apply a single entry for the given group in the template.
		Return True when an entry is applied, False otherwise.
		'''
		if template is None:
			template = self.tex
		#template = tex[start[0] + start[1]:end[0]]
		#res = template
		
		return False

	def _applyGlobal(self, data, start, end, template=None):
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
