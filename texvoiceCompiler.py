# coding: UTF-8

from inputData import Price
from texvoiceTemplateLoader import TexvoiceTemplateLoader

import subprocess, os
		
class TexvoiceCompiler(object):	
	VERSION = 2

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

	def findSection(self, name):
		start = self.content.find('\\begin{%s}' % name)
		if start is -1:
			return (-1, -1, '')
		end = self.content.find('\\end{%s}' % name)
		template = self.content[start + len(name) + 10:end-2]
		
		return (start - 1, end + 6 + len(name), template)
		
	def applyOptional(self, content, section, data, entry):
		(start, end, template) = self.findSection(section)
		if start is -1:		# No listing found
			return content
						
		if entry is None:	# Empty data
			result = ''
		else:
			result = self.applyPricing(template, entry.price)
			data['description'] = entry.description
			for key in data.keys():
				result = result.replace('\\' + key, data[key] if data[key] else '!UNKNOWN VALUE!')
				
		return content.replace(self.content[start:end], result)

	def applyOptionals(self, template, entry):
		expenses = { }
		if entry.travel:
			travel = {
				'from': entry.travel.fromLocation,
				'to': entry.travel.toLocation,
				'distance': str(entry.travel.distance),
				'price': Price.str(entry.travel.unitPrice)
			}
		else:
			travel = { }
			
		if entry.task:
			hours = {
				'price': Price.str(entry.task.wage),
				'duration': entry.task.readableDuration()
			}
		else:
			hours = { }
		
		row = self.applyOptional(template, 'expenses', expenses, entry.expenses)			
		row = self.applyOptional(row, 'travel', travel, entry.travel)			
		row = self.applyOptional(row, 'hours', hours, entry.task)
		
		return row
		
	def applyHourListing(self):
		(start, end, template) = self.findSection('texvoiceListing')
		if start is -1:		# No listing found
			return
		
		listing = ''
		
		for entry in self.inputData.entries:
			row = self.applyOptionals(template, entry)		
			row = self.applyPricing(row, entry.price)
			listing += row
			
		self.content = self.content.replace(self.content[start:end], listing)
		
		self.applyHourListing() # Recursive call for multiple listings
	
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

		pre = ''
		while not pre is self.content:
			pre = self.content
			self.content = self.applyOptionals(self.content, total)

		self.content = self.applyPricing(self.content, total.price)		
		self.content = self.replaceIfExists('\\projectID', self.inputData.project.id)
		self.content = self.replaceIfExists('\\clientName', self.inputData.project.client)
		self.content = self.replaceIfExists('\\projectDescription', self.inputData.project.description)
		self.content = self.replaceIfExists('\\invoiceID', self.inputData.invoice.id)
		
		self.content = self.replaceIfExists('\\wage', Price.str(total.task.wage))
		self.content = self.replaceIfExists('\\duration', total.task.readableDuration())
		self.content = self.replaceIfExists('\\distance', total.travel.distance)
	
	def writeResultFile(self):
		with open(self.tmpFolder + '/' + self.inputData.getResultName() + '.tex', 'w') as f:
			f.write(self.content)
		
	def compile2pdf(self):
		resultName = self.inputData.getResultName()
		sourceFile = resultName + '.tex'
		pdfName = resultName + '.pdf'
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
