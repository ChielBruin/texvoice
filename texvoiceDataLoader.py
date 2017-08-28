import argparse


class TexvoiceDataLoader(object):
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument('inputFile', help="Specify the input file")
		self.parser.add_argument('template', help="Specify the template file")
		self.parser.add_argument('outputFile', help="Specify the output file")
	
	def load(self, dataFile, template, output):
		raise Exception('Not implemented')
