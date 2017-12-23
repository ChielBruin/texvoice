from tkEditTable import TKEditTable
import tvDataLoader
import tvCompiler

from Tkinter import *


#######################
# Global testing data #
#######################

options = {
	"keepSource": ("Keep the compiled text sources", False),
	"invoiceID":  ("The ID of this invoice", ""),
	"resultFile": ("The file location where to store the result", "../result.pdf"),
	"template": ("The template to use when compiling", "../testTemplate.tex")
}



class MainApp:
	'''
	The main app. Displays all the graphic elements and handles the importing of data and calling the compilation task.
	'''
	def __init__(self):
		self.root = Tk()
		self.root.title("Texvoice V2 (developemnt build)")
		self.tables = {}
		self.optionValues = {}
		self.data = {}
	
	def draw(self):
		'''
		Draw all the graphic elements and start the main loop
		'''
		global options
		self.loadData('../timesheet2.csv', 'csv', {'configFile': '../csvConfigs/Timesheet_NL.conf'})
			
		# Draw the data tables
		self.tables["tasks"]    = self.drawTable(self.root, self.data["hours"])
		self.tables["expenses"] = self.drawTable(self.root, self.data["expenses"])
		self.tables["travel"]   = self.drawTable(self.root, self.data["travel"])
		
		# Draw the options menu
		self.optionValues = self.drawOptions(self.root, options)
		
		self.root.mainloop()
		
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
			l = lambda: tkMessageBox.showinfo(key, value[0])		# TODO: fix this button
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
		Button(frame, text="Compile", command=lambda: self.onCompile()).grid(row=len(options)//maxOptions,column=maxOptions)
		return optionValues
				
	def gatherTableData(self):
		'''
		Gather all the data from the data tables
		'''
		data = {}
		for key, table in self.tables.items():
			data[key] = table.getData()
		return data
			
	def gatherOptionData(self):
		'''
		Gather all the data from the option list
		'''
		data = {}
		for key, option in self.optionValues.items():
			data[key] = option.get()
		return data
			
	def onCompile(self):
		'''
		Gather all the needed data and comile the invoice
		'''
		compileData = {}
		compileData["data"] = self.gatherTableData()
		compileData["options"] = self.gatherOptionData()
		
		tex = tvCompiler.convert(compileData)
		print(tex)
		tvCompiler.compile(tex, compileData['options']['resultFile'], keepSource=compileData['options']['keepSource'])
	
	def loadData(self, datafile, mode, conf):
		self.data = tvDataLoader.load(datafile, mode, conf)
		

if __name__ == '__main__':
	MainApp().draw()
