from tvTemplateData import TemplateData

import tvDataLoader
import tvCompiler
import tvViews as view

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


class ScrollFrame (Frame):
	'''
	A frame for which the contents are scrollable.
	'''
	def __init__(self, root, **args):
		super(ScrollFrame, self).__init__(root, **args)
		self.canvas = Canvas(self)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
		
		scrollbar = Scrollbar(self, command=self.canvas.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		
		self.containedFrame = None

		self.canvas.configure(yscrollcommand=scrollbar.set)
		
	def attach(self, frame):
		'''
		Attach a frame to make it scrollable.
		'''
		if self.containedFrame:
			self.containedFrame.pack_forget()
		frame.bind('<Configure>', lambda x: self.onConfigure())
		self.containedFrame = frame
		
	def onConfigure(self):
		'''
		Update the scrollbar regions.
		'''
		#TODO: fix this method
		fr = self.containedFrame
		self.canvas.configure(scrollregion=(fr.winfo_height()*.8, 0, fr.winfo_width(), fr.winfo_height()))

class MainApp:
	'''
	The main app. Displays all the graphic elements and handles the importing of data and calling the compilation task.
	'''
	def __init__(self):
		root = Tk()
		root.title('Texvoice (V2 development build)')
		
		# Make it cover the entire screen
		root.geometry('%dx%d+0+0' % (root.winfo_screenwidth(), root.winfo_screenheight()))
		root.focus_set()
		root.bind('<Escape>', lambda e: e.widget.quit())
		
		self.roots = self._drawSetup(root)
	
	def _drawSetup(self, root):
		'''
		Setup the layout of the app.
		'''
		# Top panel
		menuView = view.MenuView(root)
		menuView.grid(row=0, column=0, columnspan=4, sticky=W+E)
		
		# Middle panel
		scrollFrame = ScrollFrame(root)
		scrollFrame.grid(row=1, column=0, columnspan=3, sticky=N+E+S+W)
		
		dataView = view.DataView(scrollFrame.canvas)
		scrollFrame.attach(dataView)
		dataView.pack(side=TOP)
			
		templateView = view.TemplateView(root, None)
		templateView.grid(row=1, column=3, sticky=N+E)
		
		# Bottom panel			
		optionView = view.OptionView(root)
		optionView.grid(row=2, column=0, columnspan=4, sticky=W)
		
		globalView = view.OptionView(root)
		globalView.grid(row=3, column=0, columnspan=4, sticky=W)
		
		bottomView = Frame(root)
		bottomView.grid(row=4, column=0, columnspan=4, sticky=W+E)
		Label(bottomView, text='Texvoice© Chiel Bruin').pack(side=RIGHT)
		
		root.grid_columnconfigure(0, weight='1')
		root.grid_rowconfigure(1, weight='1')
		
		return {
			'main': root,
			'templateView': templateView,
			'dataView': dataView,
			'optionView': optionView,
			'globalView': globalView,
			'menuView': menuView
			}

	def draw(self):
		'''
		Draw all the graphic elements and start the main loop
		'''
		self.drawMenu()
		self.roots['optionView'].setOptions([
			{
				'name': 'keepSource',
				'desc': 'Keep the latex file that is compiled',
				'type': 'bool',
				'default': False
			}, {
				'name': 'resultFile',
				'desc': 'The location to store the desired result',
				'type': 'string',
				'default': 'result.pdf'
			}
		])
		self.roots['main'].mainloop()
			
	def drawMenu(self):	
		'''
		Add all the menu buttons to the menu.
		'''	
		def btn_templateSelect():
			'''
			Prompt the user to select the template and load this template.
			'''
			file = filedialog.askopenfilename(title = 'choose your template',filetypes = (('texvoice templates','*.zip'),('all files','*.*')))
			if file:
				try:
					self.template = TemplateData(file)
					self.roots['templateView'].setTemplate(self.template)
					
					# Display empty tables when needed
					dataView = self.roots['dataView']
					requiredData = self.template.getProperty('requiredGroups')
					data = {}
					for group in requiredData:
						data[group] = {'keys': requiredData[group], 'data': []}
					dataView.setData(data)
					
					# Set the required options
					self.roots["globalView"].setOptions(self.template.getProperty('requiredFields'))
				except Exception as e:
					messagebox.showerror('Error loading template', e)
		
		def btn_dataSelect():
			'''
			Prompt the user for a data file to load and display the loaded data.
			'''
			file = filedialog.askopenfilename(title = 'choose your input data', filetypes=tvDataLoader.acceptedFiles())
			if file:
				try:
					data = tvDataLoader.load(file, file.split('.')[-1])
					
					dataView = self.roots['dataView']
					dataView.setData(data, override=True)					
					
				except Exception as e:
					messagebox.showerror('Loading data failed', e)
		
		def btn_compile():
			'''
			Compile and process the results.
			'''
			(result, info) = self.onCompile()
			if result:
				messagebox.showinfo('Compilation successful', 'The document successfully compiled')
			else:
				messagebox.showerror('Compilation failed', info)
		
		# Add keybindings
		root = self.roots['main']
		root.bind("<Control-c>", lambda e: btn_compile())
		root.bind("<Control-d>", lambda e: btn_dataSelect())
		root.bind("<Control-t>", lambda e: btn_templateSelect())
		
		# Add buttons
		menu = self.roots['menuView']
		menu.addButton("Select template", command=btn_templateSelect)
		menu.addButton("Select input data", command=btn_dataSelect)
		menu.addButton("Compile", side=RIGHT, command=btn_compile)
		
	def onCompile(self):
		'''
		Gather all the needed data and comile the invoice
		'''
		template = self.roots['templateView'].template
		if not template:
			return (False, 'No template selected')
		
		if not tvCompiler.checkTemplateVersion(template.getProperty('compilerVersion')):
			return (False, 'The selected template is not compatible with the current compiler')			
			
		try:
			compileData = {}
			compileData['data']    = self.roots['dataView'].getData()
			compileData['options'] = self.roots['optionView'].getData()
			compileData['global']  = self.roots['globalView'].getData()
			
			compileData['options']['template'] = template.templateFile
			
			tex = tvCompiler.convert(compileData)
			return tvCompiler.compile(tex, compileData['options'])
		except Exception as e:
			return (False, str(e))

