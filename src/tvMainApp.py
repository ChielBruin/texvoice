from tkEditTable import TKEditTable
from tvTemplate import Template

import tvDataLoader
import tvCompiler

from tkinter import *
from tkinter import messagebox


class MainApp:
	'''
	The main app. Displays all the graphic elements and handles the importing of data and calling the compilation task.
	'''
	def __init__(self):
		self.root = Tk()
		self.root.title("Texvoice V2 (development build)")
		self.tables = {}
		self.optionValues = {}
		self.data = {}
	
	def draw(self, options):
		'''
		Draw all the graphic elements and start the main loop
		'''
		self.loadTemplate(options['template'])
		fields = self.template.requiredFields
		
		self.loadData(options['inputFile'][1], 'csv', {'configFile': 'csvConfigs/Timesheet_NL.conf'})
			
		# Draw the data tables
		for group in self.data:
			self.tables[group] = self.drawTable(self.root, self.data[group])
		
		# Draw the options menu
		self.optionValues = self.drawOptions(self.root, options)
		self.fieldValues = self.drawFields(self.root, fields)
		
		self.root.mainloop()
	
	def loadTemplate(self, templateFile):
		self.template = Template(templateFile)
		
	def drawTable(self, root, data):
		'''
		Draw a data table for the given data
		'''
		table = TKEditTable(root, data["keys"])
		for i, row in enumerate(data["data"]):
			table.addRow(row)
		return table
		
	def drawOptions(self, root, options, maxOptions=4):
		'''
		Draw the list of options and the compile button
		'''
		frame = Frame(root)
		frame.grid()
		optionValues = {}
		
		for i, (key, value) in enumerate(options.items()):
			container = Frame(frame)
			container.grid(column=i%maxOptions, row=i//maxOptions)
			l = lambda: messagebox.showinfo(key, value[0])		# TODO: fix this button
			Button(container, text=key, highlightthickness=0, bd=0, command=l).grid(column=0, row=0)
			
			# String option
			if (type(value[1]) == str):
				var = StringVar()
				e = Entry(container, textvariable=var)
				e.grid(column=1, row=0)
				e.insert(0, value[1])
				optionValues[key] = var
				
			# Boolean option
			else :
				var = BooleanVar()
				e = Checkbutton(container, onvalue=True, offvalue=False, variable=var)
				e.grid(column=1, row=0)
				optionValues[key] = var
				
		# Add compile button
		Button(frame, text="Compile", command=lambda: 
			(lambda successful, info: messagebox.showinfo('Compilation successful', 'The document successfully compiled') if successful else messagebox.showerror('Compilation failed', info))(*self.onCompile())
		).grid(row=len(options)//maxOptions,column=maxOptions)
		return optionValues
		
	def drawFields(self, root, fields, maxOptions=4):
		'''
		Draw the list of fields
		'''
		frame = Frame(root)
		frame.grid()
		fieldValues = {}
		
		for i, (key, info) in enumerate(fields):
			container = Frame(frame)
			container.grid(column=i%maxOptions, row=i//maxOptions)
			l = lambda: messagebox.showinfo(key, info)		# TODO: fix this button
			Button(container, text=key, highlightthickness=0, bd=0, command=l).grid(column=0, row=0)
			
			var = StringVar()
			e = Entry(container, textvariable=var)
			e.grid(column=1, row=0)
			fieldValues[key] = var

		return fieldValues
	
	def gatherData(self, itemValues):
		'''
		Gather all the data from the given list
		'''
		data = {}
		for key, option in itemValues.items():
			data[key] = option.get()
		return data
			
	def onCompile(self):
		'''
		Gather all the needed data and comile the invoice
		'''
		compileData = {}
		compileData["data"]    = self.gatherData(self.tables)
		compileData["options"] = self.gatherData(self.optionValues)
		compileData["global"]  = self.gatherData(self.fieldValues)
				
		try:
			tex = tvCompiler.convert(compileData)
			return tvCompiler.compile(tex, compileData['options'])
		except Exception as e:
			return (False, str(e))
	
	def loadData(self, datafile, mode, conf):
		self.data = tvDataLoader.load(datafile, mode, conf)
