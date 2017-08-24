# coding: UTF-8
import csv
import argparse

import texvoiceDataLoader
import inputData as idata

class TexvoiceCSVLoader(texvoiceDataLoader.TexvoiceDataLoader):
	def load(self, dataFile, template, output):
		data = idata.InputData(template, output)
		
		with open(dataFile, 'rb') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')
			for entry in reader:
				description = entry['Beschrijving']
				duration = idata.Task.parseDuration(entry['Rel. Tijdsduur'])
				wage = float(entry['Uurloon'])
				data.addTask(idata.Task(description, duration, wage))
				
		return data
	

