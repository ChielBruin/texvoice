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
		root.geometry("%dx%d+0+0" % (root.winfo_screenwidth(), root.winfo_screenheight()))
		
		root.focus_set()
		root.bind("<Escape>", lambda e: e.widget.quit())
		
		self.roots = self._drawSetup(root)
	
	def _drawSetup(self, root):
		# Top panel
		menuView = view.MenuView(root, background='#00FF77')
		menuView.pack(fill=X)
		
		# Middle panel
		container = Frame(root)
		container.pack(fill=BOTH, expand=True)
		
		dataCanvas = Canvas(container)
		dataCanvas.pack(side=LEFT, fill=BOTH, expand=True)
		dataView = view.DataView(dataCanvas, background='#0000FF')
		dataView.pack(fill=BOTH)
		
		sb = Scrollbar(container,orient="vertical", command=dataCanvas.yview)
		sb.pack(side=LEFT, fill=Y)
		dataCanvas.configure(yscrollcommand=sb.set)
		
		templateView = view.TemplateView(container, None, background='#FF0077')
		templateView.pack(side=RIGHT, fill=BOTH, expand=True)
		
		# Bottom panel
		bottomView = Frame(root)
		bottomView.pack(side=BOTTOM, fill=X)
		Label(bottomView, text='Texvoice© Chiel Bruin').pack(side=RIGHT)
			
		optionView = view.OptionView(root, background='#55FF77')
		optionView.pack(fill=X, side=BOTTOM)
		
		globalView = view.OptionView(root, background='#55FFFF')
		globalView.pack(fill=X, side=BOTTOM)
		
			
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
		
		# Add buttons
		menu = self.roots['menuView']
		menu.addButton("Select template", command=btn_templateSelect)
		menu.addButton("Select input data", command=btn_dataSelect)
		menu.addButton("Compile", side=RIGHT, command=lambda:btn_compile(*self.onCompile()))
		
	def onCompile(self):
		'''
		Gather all the needed data and comile the invoice
		'''
		compileData = {}
		compileData['data']    = self.roots['dataView'].getData()
		compileData['options'] = self.roots['optionView'].getData()
		compileData['global']  = self.roots['globalView'].getData()
		
		compileData['options']['template'] = self.roots['templateView'].template.templateFile
				
		try:
			tex = tvCompiler.convert(compileData)
			return tvCompiler.compile(tex, compileData['options'])
		except Exception as e:
			return (False, str(e))

