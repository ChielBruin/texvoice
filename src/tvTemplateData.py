import zipfile, json
from tkinter import PhotoImage
from tkinter import *


class TemplateData:
	def __init__(self, templateFile):
		self.templateFile = templateFile
		
		if not zipfile.is_zipfile(templateFile):
			raise Exception(templateFile + ' is not a .zip file')
			
		with zipfile.ZipFile(templateFile,"r") as zf:
			containedFiles = zf.namelist()
			if not set(['properties.json', 'example.png']).issubset(set(containedFiles)):
				raise Exception('Malformed template')
				
			with zf.open('properties.json') as propertiesFile:
				jsonString = propertiesFile.read().decode('UTF-8')
				self._properties = json.loads(jsonString)
			
			self.img = PhotoImage(data=zf.open('example.png').read(), format='png')
			
	def getProperty(self, prop):
		if prop in self._properties:
			return self._properties[prop]
		else:
			return None

