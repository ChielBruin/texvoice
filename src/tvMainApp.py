from tvTemplateData import TemplateData

import tvDataLoader
import tvCompiler
import tvViews as view

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

class MainApp:
	'''
	The main app. Displays all the graphic elements and handles the importing of data and calling the compilation task.
	'''
	def __init__(self):
		root = Tk()
		root.title('Texvoice (V2 development build)')
		
		# make it cover the entire screen
		root.geometry('%dx%d+0+0' % (root.winfo_screenwidth(), root.winfo_screenheight()))
		root.focus_set()
		root.bind('<Escape>', lambda e: e.widget.quit())
		
		self.roots = self._drawSetup(root)
	
	def _drawSetup(self, root):
		# Top panel
		menuView = view.MenuView(root)
		menuView.pack(fill=X, pady=10, padx=5)
		
		# Middle panel
		container = Frame(root)
		container.pack(fill=BOTH, expand=True, pady=10)
		
		dataCanvas = Canvas(container)
		dataCanvas.pack(side=LEFT, fill=BOTH, expand=True)
		dataView = view.DataView(dataCanvas)
		dataView.pack(fill=BOTH, padx=10, pady=10)
		
		sb = Scrollbar(container, orient="vertical", command=dataCanvas.yview)
		sb.pack(side=LEFT, fill=Y)
		dataCanvas.configure(yscrollcommand=sb.set)
		
		templateView = view.TemplateView(container, None)
		templateView.pack(side=RIGHT, fill=Y)
		
		# Bottom panel
		bottomView = Frame(root)
		bottomView.pack(side=BOTTOM, fill=X)
		Label(bottomView, text='Texvoice© Chiel Bruin').pack(side=RIGHT)
			
		optionView = view.OptionView(root)
		optionView.pack(fill=X, side=BOTTOM, pady=10)
		
		globalView = view.OptionView(root)
		globalView.pack(fill=X, side=BOTTOM, pady=10)
		
			
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
		def btn_templateSelect():
			file = filedialog.askopenfilename(title = 'choose your template',filetypes = (('texvoice templates','*.zip'),('all files','*.*')))
			if file:
				try:
					self.template = TemplateData(file)
					self.roots['templateView'].setTemplate(self.template)
					dataView = self.roots['dataView']
					requiredData = self.template.getProperty('requiredGroups')
					data = {}
					for group in requiredData:
						data[group] = {'keys': requiredData[group], 'data': []}
					dataView.setData(data)
					self.roots["globalView"].setOptions(self.template.getProperty('requiredFields'))
				except Exception as e:
					messagebox.showerror('Error loading template', e)
		
		def btn_dataSelect():
			file = filedialog.askopenfilename(title = 'choose your input data', filetypes=tvDataLoader.acceptedFiles())
			if file:
				try:
					data = tvDataLoader.load(file, file.split('.')[-1])
					
					dataView = self.roots['dataView']
					dataView.setData(data, override=True)					
					
				except Exception as e:
					messagebox.showerror('Loading data failed', e)
		
		def btn_compile(result, info):
			if result:
				messagebox.showinfo('Compilation successful', 'The document successfully compiled')
			else:
				messagebox.showerror('Compilation failed', info)
		
		# Add keybindings
		compileLambda = lambda:btn_compile(*self.onCompile())
		root = self.roots['main']
		root.bind("<Control-c>", lambda e: compileLambda())
		root.bind("<Control-d>", lambda e: btn_dataSelect())
		root.bind("<Control-t>", lambda e: btn_templateSelect())
		
		# Add buttons
		menu = self.roots['menuView']
		menu.addButton("Select template", command=btn_templateSelect)
		menu.addButton("Select input data", command=btn_dataSelect)
		menu.addButton("Compile", side=RIGHT, command=compileLambda)
		
	def onCompile(self):
		'''
		Gather all the needed data and comile the invoice
		'''
		template = self.roots['templateView'].template
		if not template:
			return (False, 'No template selected')
			
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

