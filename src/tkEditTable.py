from Tkinter import *


class TKEditTable:
	'''
	Class for displaying a mutable data table.
	The table has a header and each row can be eddited or even removed.
	The first row acts as an input field for new rows.
	'''
	def __init__(self, tkroot, header):
		self.root = Frame(tkroot)
		self.root.grid()
		
		self.width = len(header)
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
			if (isinstance(e, Button)):
				continue
			data.append(e.get())
			e.delete(0, END) 
		self.addRow(data)
			
		
	def _addHeader(self, titles):
		'''
		Add the header to the table
		'''
		if(self.root.grid_slaves(row=0)):
			raise Exception("The header must be the first element in the table")

		for i in range(len(titles)):
			title = titles[i]
			if '(' in title:
				title = title.split('(')[0]
			Label(self.root, text=title.upper()).grid(row=0, column=i)
		
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
		rowID = self.height
		self._addRow(row, lambda: self.deleteRow(rowID), "X")
		
	def deleteRow(self, idx):
		'''
		Delete the row at position idx
		'''
		# TODO: Display are you sure prompt
		print(idx)
		# TODO: Actually remove the row		
	
	def get(self):
		'''
		Returns a 2D array containing all the currently stored data
		'''
		res = []
		for i in range(self.height):
			row = self.root.grid_slaves(row=i+2)
			rowRes = []
			for i, entry in enumerate(reversed(row)):
				if not (isinstance(entry, Button)):
					rowRes.append(entry.get())
			res.append(rowRes)
		return {"keys": self.keys ,"data": res}
