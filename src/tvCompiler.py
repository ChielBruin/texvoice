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
	globalData = generateGlobalData(data)
	
	template = loadTemplate(inputData['options']['template'])
	
	template.applyListings(data)
	template.applyGlobal(globalData)
	template.applyOptions(options)
	
	return template.tex

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
	return version in [2, 3]
	
def generateGlobalData(data):
	'''
	Generate the totals from the data.
	'''
	return {}
