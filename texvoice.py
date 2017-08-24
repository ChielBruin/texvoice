from texvoiceCSVLoader import TexvoiceCSVLoader
from texvoiceCompiler import TexvoiceCompiler
from texvoiceTemplateLoader import TexvoiceTemplateLoader
from texvoiceDataLoader import TexvoiceDataLoader
from inputData import InputData

import os, sys
import argparse

_VERSION = 1

def getLoader(name):
	loaders = {
		'CSV': TexvoiceCSVLoader()
	}
	i = name.find('.')
	ex = name[i+1:]
	return loaders[ex.upper()]
	
if __name__ == '__main__':
	argv = sys.argv[1:]
	if len(argv) < 4:
		raise ValueError('Please specify an input mode, input file, template and output file')
	loader = getLoader(argv[0])
	argv[3] = argv[3].split('.')[0]
	data = loader.load(*argv[1:4])
	TexvoiceDataLoader.applyArgs(data, argv[4:])
	
	(content, version) = TexvoiceTemplateLoader.loadTemplate(data.invoice.templateName)
	
	if version < _VERSION:
		print('You are using an old template, things might be broken')
	
	compiler = TexvoiceCompiler('.tmp', content, data)
	compiler.compile()
	
	
