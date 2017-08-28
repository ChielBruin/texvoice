# coding: UTF-8

import os, shutil
from zipfile import ZipFile

class TexvoiceTemplateLoader(object):
	tmpFolder = '.tmp'
	
	@classmethod
	def loadTemplate(cls, template):
		cls.unpack(template + '.zip')
		
		(res, templateVersion) = cls.validate()
		if res == True:
			return (cls.readTemplateFile(), templateVersion)
		else:
			cls.cleanup()
			raise res

	@classmethod
	def validate(cls):
		# Check if files exist
		if not os.path.isfile(cls.tmpFolder + '/VERSION'):
			return (Exception('The template does not contain a VERSION file'), -1)	
		if not os.path.isfile(cls.tmpFolder + '/template.tex'):
			return (Exception('The template does not contain a template.tex file'), -1)
		if not os.path.isfile(cls.tmpFolder + '/example.pdf'):
			return (Exception('The template does not contain an example pdf'), -1)
			
		# Check version
		with open(cls.tmpFolder + '/VERSION' , 'r') as infile:
			line = infile.readline()
			if 'texvoiceVersion=' not in line:
				return (Exception('Invalid VERSION file'), -1)
			version = int(line[line.find('texvoiceVersion=')+17:])

		return (True, version)
		
	@classmethod
	def cleanup(cls):
		shutil.rmtree('.tmp')
	
	@classmethod
	def unpack(cls, templateZip):
		with ZipFile(templateZip, 'r') as archive:
			archive.extractall(cls.tmpFolder)
	
	@classmethod
	def readTemplateFile(cls):
		content = ''	
		with open(cls.tmpFolder + '/template.tex' , 'r') as infile:
			line = infile.readline()
			while line:
				content += line
				line = infile.readline()
		return content
