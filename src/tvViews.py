from tkinter import *
from tkinter import messagebox

from tkEditTable import TKEditTable


class TemplateView (Frame):
	def __init__(self, root, template, **args):
		super(TemplateView, self).__init__(root, **args)
		self.template = template
	
	def setTemplate(self, template):
		self.template = template
		#TODO: Display the template preview + data
		
class DataView (Frame):
	def __init__(self, root, **args):
		super(DataView, self).__init__(root, **args)
		self.tables = {}
		
	def addTable(self, group, keys):
		if group in self.tables:
			raise Exception('You cannot have two groups with the same name')
		table = TKEditTable(self, keys)
		table.pack()
		self.tables[group] = table
		return table
	
	def addRow(self, group, data):
		self.tables[group].addRow(data)
		
	def checkKeys(self, group, keys):
		if group in self.tables:
			if not self.tables[group].checkKeys(keys):
				raise Exception('Template not compatible with the selected data')
		else:
			self.addTable(group, keys)
	
	def setData(self, data, override=False):
		# Only set when there is no data stored, except when override is set 
		if self.tables and (not override):
			return
		
		# Remove current contents
		for group in self.tables:
			self.tables[group].pack_forget()
		self.tables = {}
			
		for group in data:
			table = self.addTable(group, data[group]['keys'])

			# Add the data
			for i, row in enumerate(data[group]['data']):
				table.addRow(row)
		
	def getData(self):
		data = {}
		for key, option in self.tables.items():
			data[key] = option.get()
		return data
		
class MenuView (Frame):
	def __init__(self, root, **args):
		super(MenuView, self).__init__(root, **args)
	
	def addButton(self, text, command=None, side=LEFT):
		Button(self, text=text, command=command).pack(side=side)
	
class ValueView (Frame):
	def __init__(self, root, **args):
		super(ValueView, self).__init__(root, **args)
		self.values = {}
		
	def _clear(self):
		for child in self.pack_slaves():
			child.pack_forget() 
		self.values = {}
		
	def getData(self):
		result = {}
		for field in self.fieldValues:
			result[field] = self.fieldValues[field].get()
		return result
		
class OptionView (ValueView):
	def __init__(self, root, **args):
		super(OptionView, self).__init__(root, **args)
		self.values = {}
		
	def setOptions(self, options):
		self._clear()
		
		for i, option in enumerate(options):
			key = option['name']
			info = option['desc']
			type = 'string'
			if 'type' in option:
				type = option['type']
				
			container = Frame(self)
			container.pack(side=LEFT)
			l = lambda: messagebox.showinfo(key, info)		# TODO: fix this button
			Button(container, text=key, highlightthickness=0, bd=0, command=l).pack(side=LEFT)
			
			# String option
			if type == 'string':
				var = StringVar()
				e = Entry(container, textvariable=var)
				e.pack(side=LEFT)
				self.values[key] = var
				if 'default' in option:
					e.insert(0, option['default'])
				
			# Boolean option
			elif type == 'bool':
				var = BooleanVar()
				e = Checkbutton(container, onvalue=True, offvalue=False, variable=var)
				e.pack(side=LEFT)
				self.values[key] = var
				if 'default' in option:
					if option['default']:
						e.select()
					else:
						e.deselect()
			else:
				raise Exception('Unknown type ' + type)
				
	def _clear(self):
		for child in self.pack_slaves():
			child.pack_forget()
		self.values = {}
		
	def getData(self):
		result = {}
		for field in self.values:
			result[field] = self.values[field].get()
		return result
