from texvoiceCSVLoader import TexvoiceCSVLoader
from texvoiceCompiler import TexvoiceCompiler
from texvoiceTemplateLoader import TexvoiceTemplateLoader
from texvoiceDataLoader import TexvoiceDataLoader
from inputData import InputData

import sys
import argparse

def getLoader(name):
	loaders = {
		'CSV': TexvoiceCSVLoader()
	}
	if not name in loaders:
		print('Unknown mode\nUse any of the following modes: ' + ', '.join(loaders.keys()))
		exit(1)
	
	return loaders[name]

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print('Please specify the data mode')
		exit(1)
		
	loader = getLoader(sys.argv[1])
	data = loader.load(sys.argv[2:])
	
	(content, version) = TexvoiceTemplateLoader.loadTemplate(data.invoice.templateName)
	
	if not TexvoiceCompiler.VERSION in version:
		print('You are using a template that is designed for another version of the compiler, things might be broken')
	
	compiler = TexvoiceCompiler('.tmp', content, data)
	compiler.compile()
	
	
