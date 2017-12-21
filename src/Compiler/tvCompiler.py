import texcaller

def bigStep(inputData, template, resultFile):
	'''
	Convert and compile in a single step.
	'''
	latex = convert(inputData, template)
	return compile(latex, resultFile, keepSource=inputData['options']['keepSource'])
	
def convert(inputData, template):
	'''
	Convert the template and the data to a .tex file that can be compiled
	'''
	options = inputData['options']
	data = inputData['data']
	globalData = generateGlobalData(data)
	
	result = template
	listings = getListings(template)
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
	
	return info
	
def generateGlobalData(data):
	'''
	Generate the totals from the data.
	'''
	return {}
	
def getListings(tex):
	'''
	Get a list of the positions of all the listings in the input
	'''
	return [(0, 0)]
	
def applyListing(start, end, tex, data):
	'''
	Apply as much of the data as is possible in the given range.
	Returns the result and the data that couldn't be applied.
	'''
	return (tex, data)
	
def applyGlobalData(tex, data)
	'''
	Apply all the global data to the input.
	'''
	return tex

def applyOptions(tex, options)
	'''
	Apply all the options to the input.
	'''
	return tex
