import texcaller


def loadTemplate(templateFile):
	'''
	Load the specified template file from disk.
	'''
	with open(templateFile, 'r') as f:
		return f.read()
	
def convert(inputData):
	'''
	Convert the template and the data to a .tex file that can be compiled
	'''
	options = inputData['options']
	data = inputData['data']
	globalData = generateGlobalData(data)
	
	result = loadTemplate(inputData['options']['template'])
	listings = getListings(result)
	for (start, end) in listings:
		(result, data) = applyListing(start, end, result, data)
		
	result = applyGlobalData(result, globalData)
	result = applyOptions(result, options)
	
	return result

def compile(latex, resultFile, keepSource=False):
	'''
	Compile the given .tex input to PDF and store the result in the given file location
	'''
	pdf, info = texcaller.convert(latex, 'LaTeX', 'PDF', 5)

	with open(resultFile, 'w') as f:
		f.write(pdf)
	
	return (not (pdf is []), info)
	
def checkTemplateVersion(version):
	'''
	Check if the given template version is compatible with the compiler.
	'''
	return version in [2]
	
def generateGlobalData(data):
	'''
	Generate the totals from the data.
	'''
	return {}

def findSection(tex, name, beg=0):
	'''
	Find a section with a given name in the input.
	When a starting point is given only returns a section after that point
	'''		
	startStr = '\\begin{%s}' % name
	endStr = '\\end{%s}' % name
	
	start = tex.find(startStr, beg)
	if start is -1:
		return ((-1, len(startStr)), (-1, len(endStr)))
	end = tex.find(endStr, start)
	if end is -1:
		raise Exception('Cannot find closing tag for %s' % name)
	return ((start, len(startStr)), (end, len(endStr)))
	
def getListings(tex):
	'''
	Get a list of the positions of all the listings in the input
	'''
	res = []
	finger = 0
	while (True):
		(start, end) = findSection(tex, 'texvoiceListing', finger)
		if (start[0] is -1):
			return res
		else:
			finger = end[0] + end[1]
			res.append((start, end))
	
def applyListing(start, end, tex, data):
	'''
	Apply as much of the data as is possible in the given range.
	Returns the result and the data that couldn't be applied.
	'''
	
	def applyListingGroup(data, group, start, end, template):
		'''
		Apply a single entry for the given group in the template.
		Return True when an entry is applied, False otherwise.
		'''
		template = tex[start[0] + start[1]:end[0]]
		res = template
		
		return (False, tex[:start[0]] + res + tex[end[0] + end[1]:])
	
	def applyListingGlobal(data, template):
		'''
		Apply a the global data in the template.
		Return True when data is applied, False otherwise.
		'''
		for group in data:
			# TODO: Apply the accumulative data for each group
			pass
		# TODO: Apply the global accumulatives
		return (False, template)
	
	template = tex[start[0] + start[1]:end[0]]
	res = ''
	
	while True:
		(didApplyGroup, tmp) = (False, template)
		
		# For each group
		for group in data:
			(groupStart, groupEnd) = findSection(template, group)
			if (groupStart[0] is -1):
				continue
			(didApplyGroup, tmp) = applyListingGroup(data, group, groupStart, groupEnd, tmp)
		
		# Global accumulates
		(didApplyGlobal, tmp) = applyListingGlobal(data, tmp)
		
		# If you did apply anythng store it otherwise we are done 
		if didApplyGlobal or didApplyGroup:
			 res += tmp
		else:
			break
	
	return (tex[:start[0]] + res + tex[end[0] + end[1]:], data)
	
def applyGlobalData(tex, data):
	'''
	Apply all the global data to the input.
	'''
	return tex

def applyOptions(tex, options):
	'''
	Apply all the options to the input.
	'''
	return tex
