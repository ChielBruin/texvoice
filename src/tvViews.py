from tkinter import *
from tkinter import messagebox

from tkEditTable import TKEditTable

class FrameView(Frame):
	'''
	A frame extended with some utility methods.
	'''
	def __init__(self, root, **args):
		super(FrameView, self).__init__(root, **args)
		
	def _clear(self):
		'''
		Remove all the children of this instance.
		'''
		for child in self.pack_slaves():
			child.pack_forget()
		
class TemplateView (FrameView):
	'''
	The view displaying the template information.
	'''
	def __init__(self, root, template, **args):
		super(TemplateView, self).__init__(root, **args)
		self.template = template
	
		Frame(self, background='#555555', width=200, height=200).pack(pady=10)
		Label(self, text='Please select a template file', width=35).pack(pady=10)
		
	def setTemplate(self, template):
		'''
		Update the displayed template.
		'''
		self.template = template
		self._clean()
			
		# Preview icon	
		Label(self, image=template.img).pack(pady=10)
		
		def add(root, field, value, rowIndex):
			Label(root, text=field, font=('bold')).grid(row=rowIndex, column=0, sticky=NW, padx=10, pady=10)
			Label(root, text=value, wraplength='4c').grid(row=rowIndex, column=1, sticky=NW, padx=10, pady=10)
		
		# Add standard fields
		grid = Frame(self)
		grid.pack(pady=10)
		i = 0
		for field in ['name', 'description', 'author', 'license']:
			add(grid, field, template.getProperty(field), i)
			i += 1
		
		# Add extra fields
		grid = Frame(self)
		grid.pack(pady=10)	
		i = 0
		for element in template.getProperty('extraData'):
			add(grid, element['name'], element['content'], i)
			i += 1
		
class DataView (FrameView):
	'''
	View displaying the data tables.
	'''
	def __init__(self, root, **args):
		super(DataView, self).__init__(root, **args)
		self.tables = {}
		self.addTable('No data selected, please import a template or load some data.', [])
		self.tables = {}	# Make sure the dummy text is correctly overwritten
		
	def addTable(self, group, keys):
		'''
		Add a table to the view for the given group, containing the keys.
		'''
		if group in self.tables:
			raise Exception('You cannot have two groups with the same name')
		
		Label(self, text=group, font=(20)).pack(padx=10, pady=10)
		table = TKEditTable(self, keys)
		table.pack(anchor=NW, padx=10, pady=10)
		self.tables[group] = table
		return table
	
	def addRow(self, group, data):
		'''
		Add a row to the table for the given group.
		'''
		self.tables[group].addRow(data)
	
	def setData(self, data, override=False):
		'''
		Set the data to a new set of data.
		When override is true it will override all the existing data.
		'''
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
		'''
		Get all the data from all the tables
		'''
		data = {}
		for key, option in self.tables.items():
			data[key] = option.get()
		return data
		
class MenuView (FrameView):
	'''
	The view containing all menu buttons.
	'''
	def __init__(self, root, **args):
		super(MenuView, self).__init__(root, **args)
	
	def addButton(self, text, command=None, side=LEFT):
		'''
		Add a button to the menu.
		'''
		Button(self, text=text, command=command).pack(side=side, padx=5)
		
class OptionView (FrameView):
	'''
	View displaying a list of options the user can interact with.
	'''
	def __init__(self, root, **args):
		super(OptionView, self).__init__(root, **args)
		self.values = {}
		
	def setOptions(self, options):
		'''
		Set the options and display them.
		'''
		self._clear()
		bgColor = '#BBBBBB'
		
		# For each option
		for i, option in enumerate(options):
			key = option['name']
			info = option['desc']
			type = 'string'
			if 'type' in option:
				type = option['type']
			
			# Create container and name label	
			container = Frame(self, background=bgColor)
			container.pack(side=LEFT, padx=5, ipady=2, ipadx=2)
			l = lambda: messagebox.showinfo(key, info)		# TODO: fix this button
			Button(container, text=key, highlightthickness=0, bd=0, command=l, background=bgColor).pack(side=LEFT)
			
			# Field for string option
			if type == 'string':
				var = StringVar()
				e = Entry(container, textvariable=var, background=bgColor)
				e.pack(side=LEFT)
				self.values[key] = var
				if 'default' in option:
					e.insert(0, option['default'])
				
			# Field for boolean option
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
		'''
		Get the data from all the options.
		'''
		result = {}
		for field in self.values:
			result[field] = self.values[field].get()
		return result
