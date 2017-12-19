from tkinter import *

class TKEditTable:
	'''
	Class for displaying a mutable data table.
	The table has a header and each row can be eddited or even removed.
	The first row acts as an input field for new rows.
	'''
	def __init__(self, tkroot, width, header):
		self.root = Frame(tkroot)
		self.root.pack()
		self.width = width
		self._addHeader(header)
		self._addRow([""]*self.width, lambda: self._commitRow(), "->")
	
	def _commitRow(self):
		'''
		Helper function to commit the input row to the table.
		'''
		row = self.root.pack_slaves()[1]
		data = []
		for i, e in enumerate(row.pack_slaves()):
			if (i >= self.width):
				break
			data.append(e.get())
			e.delete(0, END) 
		self.addRow(data)
			
		
	def _addHeader(self, titles):
		'''
		Add the header to the table
		'''
		if (len(titles) != self.width):
			raise Exception("Size mismatch")
		if(len(self.root.pack_slaves()) > 0):
			raise Exception("The header must be the first element in the table")
			
		# TODO: Spacing the titles correctly
		frame = Frame(self.root)
		frame.pack(side=TOP, fill=X)
		for i in range(len(titles)):
			Label(frame, text=titles[i].upper()).pack(side=LEFT)
		
	def _addRow(self, row, buttonLambda, token):
		'''
		Add a row to the table containing the data in 'row' and a button with the text 'token' and function 'buttonLambda'.
		'''
		if (len(row) != self.width):
			raise Exception("Size mismatch")
		
		frame = Frame(self.root)
		frame.pack(side=TOP, fill=X)
		for i in range(len(row)):
			entry = Entry(frame)
			entry.pack(side=LEFT)
			entry.insert(0, str(row[i]))
		Button(frame, text=str(token), command=buttonLambda).pack(side=LEFT)
		
	def addRow(self, row):
		'''
		Add a row to the table containing 'row' as data and a delete button for the row
		'''
		rowID = len(self.root.pack_slaves()) - 2
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
		for row in self.root.pack_slaves():
			if (type(row.pack_slaves()[0]) == Label):
				continue
			rowRes = []
			for i, entry in enumerate(row.pack_slaves()):
				if (i >= self.width):
					break
				rowRes.append(entry.get())
			res.append(rowRes)
		return res










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
	Entry(root).pack()
	drawTasks(root, tasks)

	root.mainloop()

if __name__ == '__main__':
	main()
