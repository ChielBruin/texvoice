# coding: UTF-8
import csv

import texvoiceDataLoader
import inputData as idata

class TexvoiceCSVLoader(texvoiceDataLoader.TexvoiceDataLoader):
	def load(self, dataFile, template, output, args):
		self.data = idata.InputData(template, output)
		
		with open(dataFile, 'rb') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')
			for entry in reader:
				description = entry['Beschrijving']
				duration = idata.Task.parseDuration(entry['Rel. Tijdsduur'])
				wage = float(entry['Uurloon'])
				self.data.addTask(idata.Task(description, duration, wage))
				
		self.applyArgs(args)
		return self.data

	def applyArgs(self, args):
		self.data.invoice.id = '02'
		self.data.project.id = 'MTIS'
		self.data.project.client = 'M-TIS'
		self.data.project.description = ''


