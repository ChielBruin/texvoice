from tkinter import *
from tkinter import messagebox

from tkEditTable import TKEditTable

class FrameView(Frame):
	def __init__(self, root, **args):
		super(FrameView, self).__init__(root, **args)
		
	def _clear(self):
		for child in self.pack_slaves():
			child.pack_forget()
		
class TemplateView (FrameView):
	def __init__(self, root, template, **args):
		super(TemplateView, self).__init__(root, **args)
		self.template = template
	
		Frame(self, background='#555555', width=200, height=200).pack(pady=10)
		Label(self, text='Please select a template file', width=35).pack(pady=10)
		
	def setTemplate(self, template):
		self.template = template
		
		for child in self.pack_slaves():
			child.pack_forget()
				
		Label(self, image=template.img).pack(pady=10)
		
		def add(root, field, value, rowIndex):
			Label(root, text=field, font=('bold')).grid(row=rowIndex, column=0, sticky=NW, padx=10, pady=10)
			Label(root, text=value, wraplength='4c').grid(row=rowIndex, column=1, sticky=NW, padx=10, pady=10)
		
		grid = Frame(self)
		grid.pack(pady=10)
		i = 0
		for field in ['name', 'description', 'author', 'license']:
			add(grid, field, template.getProperty(field), i)
			i += 1
		
		grid = Frame(self)
		grid.pack(pady=10)	
		i = 0
		for element in template.getProperty('extraData'):
			add(grid, element['name'], element['content'], i)
			i += 1
		
class DataView (FrameView):
	def __init__(self, root, **args):
		super(DataView, self).__init__(root, **args)
		self.tables = {}
		self.addTable('No data selected, please import a template or load some data.', [])
		self.tables = {}
		
	def addTable(self, group, keys):
		if group in self.tables:
			raise Exception('You cannot have two groups with the same name')
		
		Label(self, text=group, font=(20)).pack(padx=10, pady=10)
		table = TKEditTable(self, keys)
		table.pack(anchor=NW, padx=10, pady=10)
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
		self._clear()
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
		
class MenuView (FrameView):
	def __init__(self, root, **args):
		super(MenuView, self).__init__(root, **args)
	
	def addButton(self, text, command=None, side=LEFT):
		Button(self, text=text, command=command).pack(side=side, padx=5)
		
class OptionView (FrameView):
	def __init__(self, root, **args):
		super(OptionView, self).__init__(root, **args)
		self.values = {}
		
	def setOptions(self, options):
		self._clear()
		
		bgColor = '#BBBBBB'
		for i, option in enumerate(options):
			key = option['name']
			info = option['desc']
			type = 'string'
			if 'type' in option:
				type = option['type']
				
			container = Frame(self, background=bgColor)
			container.pack(side=LEFT, padx=5, ipady=2, ipadx=2)
			l = lambda: messagebox.showinfo(key, info)		# TODO: fix this button
			Button(container, text=key, highlightthickness=0, bd=0, command=l, background=bgColor).pack(side=LEFT)
			
			# String option
			if type == 'string':
				var = StringVar()
				e = Entry(container, textvariable=var, background=bgColor)
				e.pack(side=LEFT)
				self.values[key] = var
				if 'default' in option:
					e.insert(0, option['default'])
				
			# Boolean option
			elif type == 'bool':
				var = BooleanVar()
				e = Checkbutton(container, onvalue=True, offvalue=False, variable=var, background=bgColor)
				e.pack(side=LEFT)
				self.values[key] = var
				if 'default' in option:
					if option['default']:
						e.select()
					else:
						e.deselect()
			else:
				raise Exception('Unknown type ' + type)
		
	def getData(self):
		result = {}
		for field in self.values:
			result[field] = self.values[field].get()
		return result
