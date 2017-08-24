# coding: UTF-8

from __future__ import division


class InputData:
	def __init__(self, templateName, resultName):
		self.project = Project()
		self.invoice = Invoice(templateName, resultName)
		self.total = Total()
		self.tasks = []
		
	def addTask(self, task):
		self.total.update(task)
		self.tasks.append(task)


class Project:
	def setID(self, id):
		self.setattr(self, 'id', id)
	
	def setClient(self, client):
		self.setattr(self, 'client', client)

	def setDescription(self, desc):
		self.setattr(self, 'description', desc)


class Invoice:
	def __init__(self, templateName, resultName):
		self.templateName = templateName
		self.resultName = resultName
		
	def setID(self, id):
		self.setattr(self, 'id', id)


class Price:		
	def __init__(self, subtotal=0, vat=None):
		self.subtotal = subtotal
		if vat:
			self.vatPercentage = vat
			self.vat = subtotal * (vat / 100.0)
			self.total = subtotal + self.vat
		else:
			self.total = subtotal


class Task:
	def __init__(self, description, duration, wage, vat=None):
		self.description = description
		self.duration = duration
		self.wage = wage
		self.price = Price(duration * wage, vat)
		
	@staticmethod
	def parseDuration(string, delimiter):
		time = map(lambda x: int(x), string.split(delimiter))
		return(float(time[0] + time[1] / float(60)))


class Total:
	def __init__(self):
		self.price = Price()
		self.hours = 0
		
	def update(self, newTask):
		p = newTask.price
		self.price.subtotal += p.subtotal
		self.price.vat += p.vat
		self.price.total += p.total
		self.price.vatPercentage = ((p.total / p.subtotal) - 1) * 100
		
		self.hours += newTask.duration
		self.wage = self.price.subtotal / self.hours
