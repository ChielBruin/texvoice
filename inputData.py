# coding: UTF-8

from __future__ import division


class InputData(object):
	def __init__(self, templateName, resultName, keepSource):
		if '.zip' in templateName:
			templateName = templateName.replace('.zip', '')
		if '.pdf' in resultName:
			resultName = resultName.replace('.pdf', '')
			
		self.project = Project()
		self.invoice = Invoice(templateName, resultName, keepSource)
		self.total = Total()
		self.tasks = []
		
	def addTask(self, task):
		self.total.update(task)
		self.tasks.append(task)


class Project(object):
	def setID(self, id):
		self.setattr(self, 'id', id)
	
	def setClient(self, client):
		self.setattr(self, 'client', client)

	def setDescription(self, desc):
		self.setattr(self, 'description', desc)


class Invoice(object):
	def __init__(self, templateName, resultName, keepSource):
		self.templateName = templateName
		self.resultName = resultName
		self.keepSource = keepSource
		
	def setID(self, id):
		self.setattr(self, 'id', id)


class Price(object):
	unit = '€'
			
	def __init__(self, subtotal=0, vat=0):
		self.subtotal = subtotal
		self.vatPercentage = vat
		self.vat = subtotal * (vat / 100.0)
		self.total = subtotal + self.vat
			
	def resetVAT(self, newVAT):
		self.vatPercentage = newVAT
		self.vat = self.subtotal * newVAT / 100
		self.total = self.subtotal + self.vat

	@classmethod
	def str(cls, amount):
		# TODO: this is kinda broken
		#if amount%1 == 0:
			#return cls.unit + str(int(amount)) + ',-'
		#else :
			#return cls.unit + "%.2f" % (amount + 0.005)	# Make sure rounding goes well
		return cls.unit + "%.2f" % amount

	def strVAT(self):
		return "%.1f" % self.vatPercentage


class Task(object):
	def __init__(self, description, duration, wage, vat):
		self.description = description
		self.duration = duration
		self.wage = wage
		self.price = Price(duration * wage, vat)
		
		self.expenses = None
		self.travel = None
		
	@staticmethod
	def parseDuration(string, delimiter=':'):
		time = map(lambda x: int(x), string.split(delimiter))
		return(float(time[0] + time[1] / float(60)))
		
	def readableDuration(self, delimiter=':'):
		return str(int(self.duration)) + delimiter + "%02d" % (int((self.duration%1)*60))


class Total(Task):
	def __init__(self):
		super(Total, self).__init__(None, 0, 0, 0)
		
	def update(self, newTask):
		p = newTask.price
		self.price.subtotal += p.subtotal
		self.price.vat += p.vat
		self.price.total += p.total
		self.price.vatPercentage = ((self.price.total / self.price.subtotal) - 1) * 100
		
		self.duration += newTask.duration
		self.wage = self.price.subtotal / self.duration
