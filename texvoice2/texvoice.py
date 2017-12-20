from tkinter import *

class TKEditTable:
	'''
	Class for displaying a mutable data table.
	The table has a header and each row can be eddited or even removed.
	The first row acts as an input field for new rows.
	'''
	def __init__(self, tkroot, width, header):
		self.root = Frame(tkroot)
		self.root.grid()
		
		self.width = width
		self.keys = header
		self.height = -1	# Account for the input row
		
		self._addHeader(header)
		self._addRow([""]*self.width, lambda: self._commitRow(), "->")
	
	def _commitRow(self):
		'''
		Helper function to commit the input row to the table.
		'''
		row = self.root.grid_slaves(row=1)
		data = []
		for i, e in enumerate(reversed(row)):
			if (type(e) == Button):
				continue
			data.append(e.get())
			e.delete(0, END) 
		self.addRow(data)
			
		
	def _addHeader(self, titles):
		'''
		Add the header to the table
		'''
		if (len(titles) != self.width):
			raise Exception("Size mismatch")
		if(self.root.grid_slaves(row=0)):
			raise Exception("The header must be the first element in the table")
			
		# TODO: Spacing the titles correctly
		for i in range(len(titles)):
			Label(self.root, text=titles[i].upper()).grid(row=0, column=i)
		
	def _addRow(self, row, buttonLambda, token):
		'''
		Add a row to the table containing the data in 'row' and a button with the text 'token' and function 'buttonLambda'.
		'''
		if (len(row) != self.width):
			raise Exception("Size mismatch")
		
		for i in range(len(row)):
			entry = Entry(self.root)
			entry.grid(row=self.height+2, column=i)
			entry.insert(0, str(row[i]))
		Button(self.root, text=str(token), command=buttonLambda).grid(row=self.height+2, column=self.width)
		self.height += 1
		
	def addRow(self, row):
		'''
		Add a row to the table containing 'row' as data and a delete button for the row
		'''
		rowID = self.height + 1
		self._addRow(row, lambda: self.deleteRow(rowID), "X")
		
	def deleteRow(self, idx):
		'''
		Delete the row at position idx
		'''
		# TODO: Display are you sure prompt
		print(idx)
		# TODO: Actually remove the row		
	
	def getData(self):
		'''
		Returns a 2D array containing all the currently stored data
		'''
		res = []
		for i in range(self.height):
			row = self.root.grid_slaves(row=i+2)
			rowRes = []
			for i, entry in enumerate(reversed(row)):
				if (type(entry) == Button):
					continue
				rowRes.append(entry.get())
			res.append(rowRes)
		return {"keys": self.keys ,"data": res}










def drawTasks(root, tasks):
	table = TKEditTable(root, 3, ["Description", "Duration", "price"])
	for i, task in enumerate(tasks):
		table.addRow(task)
		
	print(table.getData())
		
		
def main():
	root = Tk()
	
	tasks = [
		["hello", 12, 13.50],
		["hella", 13, 14.50],
		["helle", 14, 15.50],
		["helly", 15, 16.50],
	]
	
	drawTasks(root, tasks)
	Entry(root).grid()
	drawTasks(root, tasks)

	root.mainloop()

if __name__ == '__main__':
	main()
