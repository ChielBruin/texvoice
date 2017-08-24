# coding: UTF-8

import os, shutil
from zipfile import ZipFile

class TexvoiceTemplateLoader(object):
	tmpFolder = '.tmp'
	
	@classmethod
	def loadTemplate(cls, template):
		cls.unpack(template)
		
		(res, templateVersion) = cls.validate()
		if res == True:
			return (cls.readTemplateFile(), templateVersion)
		else:
			cls.cleanup()
			raise res

	@classmethod
	def validate(cls):
		# TODO check if all files exist and the template version
		# return Exception('Invalid template file')
		return (True, 0)
		
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
