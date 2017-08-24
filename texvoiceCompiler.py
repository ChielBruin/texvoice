# coding: UTF-8
		
class TexvoiceCompiler():	
	def __init__(self, tmpFolder, content, inputData):
		self.tmpFolder = '.tmp'
		self.content = content
		self.inputData = inputData
		
	def compile(self, keepSource=False):
		self.applyHourListing()
		self.applyGlobalData()
		
		self.writeResultFile()
		self.compile2pdf(keepSource)
		TexvoiceTemplateLoader.cleanup()

	def applyHourListing(self):
		start = self.content.find('\\begin{hourListing}')
		end = self.content.find('\\end{hourListing}')
		template = self.content[start+21:end-2]
		listing = ''
		
		for task in self.inputData.tasks:			
			row = template.replace('\\description', task.description)	\
				.replace('\\wage', Price.str(task.wage))				\
				.replace('\\duration', task.readableDuration()) \
			self.applyPricing(row, task.price)
			listing += row
			
		self.content = self.content.replace(self.content[start:end + 17], listing)
	
	def applyIfExists(self, keyword, value, content=None):
		if not content:
			content = self.content
			
		if content.contains(keyword):
			return content.replace(keyword, value)
		else:
			return content
	
	def applyPricing(self, content, price):
		result = content.replace('\\subtotal', Price.str(price.subtotal)) 	\
			.replace('\\total', self.curr(hours * price))
		result = self.replaceIfExists('\\vatPercentage', price.vatPercentage, result)
		result = self.replaceIfExists('\\vat', price.vat, result)
	
	def applyGlobalData(self):
		total = self.inputData.total
		
		self.content = self.applyPricing(self.content, total.price)		\
			.replace('\\duration', total.duration)		\
			.replace('\\wage', Price.str(total.wage))
		
		self.content = self.replaceIfExists('\\projectID', self.inputData.project.id)
		self.content = self.replaceIfExists('\\clientName', self.inputData.project.client)
		self.content = self.replaceIfExists('\\projectDescription', self.inputData.project.description)
		self.content = self.replaceIfExists('\\invoiceID', self.inputData.invoice.id)
	
	def writeResultFile(self):
		with open(self.tmpFolder + '/result.tex', 'w') as f:
			f.write(self.content)
		
	def compile2pdf(self, keepSource):
		sourceFile = self.inputData.invoice.resultName'.tex'
		pdfName = self.inputData.invoice.resultName + '.pdf'
		resultFile = self.tmpFolder + '/' + pdfName
		
		cmd = ['pdflatex', '-interaction', 'nonstopmode', sourceFile]
		proc = subprocess.Popen(cmd, cwd=self.tmpFolder)
		proc.communicate()
		
		retcode = proc.returncode
		if not retcode == 0:
			os.remove(resultFile)
			raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
		
		os.rename(resultFile, pdfName)
		if keepSource:
			os.rename(self.tmpFolder + '/' + sourceFile, sourceFile)
