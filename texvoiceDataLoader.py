import argparse


class TexvoiceDataLoader(object):
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument('inputFile', help='Specify the input file')
		self.parser.add_argument('template', help='Specify the template file')
		self.parser.add_argument('outputFile', help='Specify the output file')
		
		
		self.parser.add_argument('--projectDescription', default=None, help='')
		self.parser.add_argument('--projectClient', default=None, help='')
		self.parser.add_argument('--projectID', default=None, help='')

		self.parser.add_argument('--invoiceID', default=None, help='')
		
		self.parser.add_argument('--VAT', type=int, default=0, dest='vat', help='')
		self.parser.add_argument('--keepSource', action="store_true", help='')
	
	def load(self, dataFile, template, output):
		raise Exception('Not implemented')

	def applyArgs(self):
		self.data.invoice.id = self.args.invoiceID
		
		self.data.project.id = self.args.projectID
		self.data.project.client = self.args.projectClient
		self.data.project.description = self.args.projectDescription
		
		if self.args.vat:
			self.data.total.resetVAT(self.args.vat)
