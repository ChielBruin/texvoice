# coding: UTF-8

from inputData import Price
from texvoiceTemplateLoader import TexvoiceTemplateLoader

import subprocess, os
		
class TexvoiceCompiler(object):	
	VERSION = 1

	def __init__(self, tmpFolder, content, inputData):
		self.tmpFolder = '.tmp'
		self.content = content
		self.inputData = inputData
		
	def compile(self):
		self.applyHourListing()
		self.applyGlobalData()
		
		self.writeResultFile()
		self.compile2pdf()
		TexvoiceTemplateLoader.cleanup()

	def applyHourListing(self):
		start = self.content.find('\\begin{hourListing}')
		end = self.content.find('\\end{hourListing}')
		template = self.content[start+21:end-2]
		listing = ''
		
		for task in self.inputData.tasks:			
			row = template.replace('\\description', task.description)	\
				.replace('\\wage', Price.str(task.wage))				\
				.replace('\\duration', task.readableDuration())
			row = self.applyPricing(row, task.price)
			listing += row
			
		self.content = self.content.replace(self.content[start:end + 17], listing)
	
	def replaceIfExists(self, keyword, value, content=None):
		if not content:
			content = self.content
			
		if keyword in content:
			return content.replace(keyword, value)
		else:
			return content
	
	def applyPricing(self, content, price):
		result = content.replace('\\subtotal', Price.str(price.subtotal)) 	\
			.replace('\\total', Price.str(price.total))
		result = self.replaceIfExists('\\vatPercentage', price.strVAT(), result)
		result = self.replaceIfExists('\\vat', Price.str(price.vat), result)
		return result
	
	def applyGlobalData(self):
		total = self.inputData.total
		
		self.content = self.applyPricing(self.content, total.price)		\
			.replace('\\duration', total.readableDuration())		\
			.replace('\\wage', Price.str(total.wage))
		
		self.content = self.replaceIfExists('\\projectID', self.inputData.project.id)
		self.content = self.replaceIfExists('\\clientName', self.inputData.project.client)
		self.content = self.replaceIfExists('\\projectDescription', self.inputData.project.description)
		self.content = self.replaceIfExists('\\invoiceID', self.inputData.invoice.id)
	
	def writeResultFile(self):
		with open(self.tmpFolder + '/' + self.inputData.invoice.resultName + '.tex', 'w') as f:
			f.write(self.content)
		
	def compile2pdf(self):
		sourceFile = self.inputData.invoice.resultName + '.tex'
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
		if self.inputData.invoice.keepSource:
			os.rename(self.tmpFolder + '/' + sourceFile, sourceFile)
