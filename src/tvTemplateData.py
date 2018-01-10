import zipfile, json
from tkinter import PhotoImage
from tkinter import *


class TemplateData:
	def __init__(self, templateFile):
		with zipfile.ZipFile(templateFile,"r") as zf:
			containedFiles = zf.namelist()
			if not set(map(lambda x: containedFiles[0]+x, ['properties.json', 'example.png'])).issubset(set(containedFiles)):
				raise Exception('Malformed template')
				
			with zf.open(containedFiles[0]+'properties.json') as propertiesFile:
				jsonString = propertiesFile.read().decode('UTF-8')
				self._properties = json.loads(jsonString)
			
			self.img = PhotoImage(data=zf.open(containedFiles[0]+'example.png').read(), format='png')
			
	def getPoperty(self, prop):
		if prop in self.properties:
			return self.properties[prop]
		else:
			return None

root = Tk()
new = TemplateData('../templateTest.zip')

panel = Label(root, image = new._img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()

