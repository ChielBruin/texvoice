import csvLoader
from tkinter import filedialog

def loadCSVConfig():
	file = filedialog.askopenfilename(title = 'choose the CSV config file',filetypes = (('config files','*.conf'),('all files','*.*')))
	return {'configFile': file}
	
modes = {
	"csv" : (csvLoader.load, loadCSVConfig)
}



def load(dataFile, mode, config=None):
	'''
	Load a specific data file in the given mode.
	'''
	with open(dataFile) as f:
		rawData = f.readlines()
		
		m = modes[mode.lower()]
		if config is None:
			return m[0](rawData, ({} if modes[mode] is None else m[1]()))
		else:
			return m[0](rawData, options)

def acceptedFiles():
	res = []
	for mode in modes:
		res.append( (mode + ' files', '*.' + mode) )
	res.append( ('all files','*.*') )
	return res
