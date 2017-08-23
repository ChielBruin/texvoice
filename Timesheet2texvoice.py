# coding: UTF-8

from texvoice import InputParser, TexCompiler

import csv
import argparse

class TimeSheetInputParser(InputParser):
	
	def __init__ (self):
		parser = argparse.ArgumentParser(description='Creates an invoice pdf from a Latex template and a TimeTable csv export')
		self.parseArgs(parser)
		
	def parseInput(self, fileName):
		with open(fileName, 'rb') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')
			for entry in reader:
				self.taskData['descriptions'].append(entry['Beschrijving'])
				
				time = map(lambda x: int(x), entry['Rel. Tijdsduur'].split(':'))	# Convert to decimal
				self.taskData['hours'].append(float(time[0] + time[1] / float(60)))
				
				self.taskData['price'].append(float(entry['Uurloon']))


if __name__ == '__main__':
	parser = TimeSheetInputParser()
	parser.parseInput('timesheet.csv')
	compiler = TexCompiler(parser, compile=True)
	
