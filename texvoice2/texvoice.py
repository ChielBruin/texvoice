from tkEditTable import TKEditTable

from tkinter import *
import tkinter.messagebox as tkMessageBox


#######################
# Global testing data #
#######################

tasks = {
	"keys": ["Description", "Duration", "price"],
	"data": [
		["hello", 12, 13.50],
		["hella", 13, 14.50],
		["helle", 14, 15.50],
		["helly", 15, 16.50],
	]
}

expenses = {
	"keys": ["Description", "price"],
	"data": [
		["bananas", 123.00],
		["apples", 2.50],
	]
}

travel = {
	"keys": ["Description", "from", "to", "distance", "price"],
	"data": [
		["back", "here", "there", 12, 12.50],
		["and forth", "there", "here", 13, 12.50],
	]
}
data = {"tasks" : tasks, "expenses": expenses, "travel": travel}
options = {
	"keepSource": ("Keep the compiled text sources", False),
	"invoiceID":  ("The ID of this invoice", ""),
	"keepSource1": ("Keep the compiled text sources", False),
	"invoiceID1":  ("The ID of this invoice", ""),
	"keepSource2": ("Keep the compiled text sources", False),
	"invoiceID2":  ("The ID of this invoice", "")		
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
	
	def draw(self):
		'''
		Draw all the graphic elements and start the main loop
		'''
		global data, options
		
		# Draw the data tables
		self.tables["tasks"]    = self.drawTable(self.root, data["tasks"])
		self.tables["expenses"] = self.drawTable(self.root, data["expenses"])
		self.tables["travel"]   = self.drawTable(self.root, data["travel"])
		
		# Draw the options menu
		self.optionValues = self.drawOptions(self.root, options)
		
		self.root.mainloop()
		self.root.destroy()
		
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
		print(compileData)
		# TODO: actually compile the document

if __name__ == '__main__':
	MainApp().draw()