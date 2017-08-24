class TexvoiceDataLoader(object):
	def load(self, dataFile, template, output):
		raise Exception('Not implemented')
		
	@staticmethod
	def applyArgs(data, args):
		print args
		data.invoice.id = '02'
		data.project.id = 'MTIS'
		data.project.client = 'M-TIS'
		data.project.description = ''
		#parser = argparse.ArgumentParser(description='Creates an invoice pdf from a Latex template and a TimeTable csv export')
		#self.parseArgs(parser)
