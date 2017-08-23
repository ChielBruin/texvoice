# coding: UTF-8

import os
import argparse
import subprocess
import shutil
from zipfile import ZipFile

class InputParser:
	projectData = None
	taskData = {
		'descriptions' : [],
		'hours' : [],
		'price' : []
	}
	
	def parseArgs(self, argparser):		
		argparser.add_argument('--output', type=str)
		argparser.add_argument('template', type=str)
		argparser.add_argument('client', type=str)
		argparser.add_argument('projectID', type=str)
		argparser.add_argument('invoiceID', type=str)
		argparser.add_argument('-VAT', type=float, default=21)
		argparser.add_argument('-projectDescription', type=str, default='')
		argparser.add_argument('-currencyPrefix', type=str, default='€')

		self.projectData = argparser.parse_args()
		
	def parseInput(self, fileName):
		raise Exception('Not implemented!')

class TexCompiler():
	projectData = None
	taskData = None
	content = ''
	
	def __init__(self, inputParser, template='template.zip', compile=False):
		self.projectData = inputParser.projectData
		self.taskData = inputParser.taskData
		
		if compile:
			self.compile(template, str(self.projectData.projectID) + '-' + str(self.projectData.invoiceID) + '.pdf')
		
	def compile(self, templateFile, resultFile):
		# TODO: Check if template is available
		self.readTexTemplate(templateFile)
		
		self.applyData(*self.applyHourListing())
		
		self.writeResultFile()
		self.compile2pdf(resultFile)
	
	def curr(self, amount):
		if amount%1 == 0:
			return self.projectData.currencyPrefix + str(int(amount)) + ',-'
		else :
			return self.projectData.currencyPrefix + "%.2f" % amount
	
	def readTexTemplate(self, templateZip):
		with ZipFile(templateZip, 'r') as zipfile:
			zipfile.extractall('.tmp')
			
		with open('.tmp/template.tex' , 'r') as infile:
			line = infile.readline()
			while line:
				self.content += line
				line = infile.readline()

	def applyHourListing(self):
		start = self.content.find('\\begin{hourListing}')
		end = self.content.find('\end{hourListing}')
		template = self.content[start+21:end-2]
		listing = ''
		listContent = \
			zip(self.taskData['descriptions'], self.taskData['hours'], [self.taskData['price']] * len(self.taskData['hours'])) if isinstance(self.taskData['price'], int) \
			else zip(self.taskData['descriptions'], self.taskData['hours'], self.taskData['price']) 
		
		totalPrice = totalHours = 0
		for (description, hours, price) in listContent:
			totalPrice += hours * price
			totalHours += hours
			
			listing += template.replace('\description', description) \
				.replace('\hours', str(int(hours)) + ':' + "%02d" % (int((hours%1)*60))) \
				.replace('\price', self.curr(price)) \
				.replace('\\total', self.curr(hours * price))
			
		self.content = self.content.replace(self.content[start:end + 17], listing)
		return (totalHours, totalPrice)
	
	def applyData(self, hours, price):
		vat = price * (self.projectData.VAT / 100.0)
		
		self.content = self.content.replace('\hoursTotal', str(hours))		\
			.replace('\\priceSubtotal', str(self.curr(price)))				\
			.replace('\\avgPrice', str(self.curr(price / float(hours))))	\
			.replace('\\VAT', str(self.projectData.VAT) + '\\%')			\
			.replace('\\priceVAT', str(self.curr(vat)))						\
			.replace('\\priceTotal', str(self.curr(price + vat)))			\
			.replace('\\clientName', str(self.projectData.client))			\
			.replace('\\projectID', str(self.projectData.projectID))		\
			.replace('\\invoiceID', str(self.projectData.invoiceID))		\
			.replace('\\projectDescription', str(self.projectData.projectDescription))	\
	
	def writeResultFile(self):
		with open('.tmp/result.tex', 'w') as f:
			f.write(self.content)
		
	def compile2pdf(self, pdfName):
		cmd = ['pdflatex', '-interaction', 'nonstopmode', 'result.tex']
		proc = subprocess.Popen(cmd, cwd='.tmp')
		proc.communicate()

		retcode = proc.returncode
		
		if not retcode == 0:
			os.remove('.tmp/result.pdf')
			os.rename('.tmp', 'tmp')
			raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
		
		os.rename('.tmp/result.pdf', pdfName)
		shutil.rmtree('.tmp')


if __name__ == '__main__':
	raise Exception('This module should not be called directly!\nPlease use one of the InputParser implementations')
	

