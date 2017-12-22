import csvLoader


modes = {
	"csv" : csvLoader.load  
}

def load(dataFile, mode, options):
	'''
	Load a specific data file in the given mode.
	'''
	with open(dataFile) as f:
		rawData = f.readlines() 
		return modes[mode.lower()](rawData, options)
