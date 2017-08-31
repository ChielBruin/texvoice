# coding: UTF-8

from __future__ import division


class InputData(object):
	def __init__(self, templateName, keepSource):
		if '.zip' in templateName:
			templateName = templateName.replace('.zip', '')
		self.project = Project()
		self.invoice = Invoice(templateName, keepSource)
		self.total = Total()
		self.entries = []
		
	def addEntry(self, task, expenses, travel):
		entry = Entry(task, expenses, travel)
		self.total.update(entry)
		self.entries.append(entry)
		
	def getResultName(self):
		return self.project.id + '-' + self.invoice.id


class Project(object):
	def setID(self, id):
		self.setattr(self, 'id', id)
	
	def setClient(self, client):
		self.setattr(self, 'client', client)

	def setDescription(self, desc):
		self.setattr(self, 'description', desc)


class Invoice(object):
	def __init__(self, templateName, keepSource):
		self.templateName = templateName
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
	
	def calcVAT(self):
		if self.subtotal == 0:
			self.vatPercentage = 0
		else:
			self.vatPercentage = ((self.total / self.subtotal) - 1) * 100

	def add(self, newPrice, updateVAT=True):
		self.subtotal += newPrice.subtotal
		self.vat += newPrice.vat
		self.total += newPrice.total
		if updateVAT:
			self.calcVAT()

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

class Entry(object):
	def __init__(self, task, expenses, travel):
		self.task = task
		self.expenses = expenses
		self.travel = travel
		
		self.price = Price()
		if task:
			self.price.add(task.price, updateVAT=False)
		if expenses:
			self.price.add(expenses.price, updateVAT=False)
		if travel:
			self.price.add(travel.price, updateVAT=False)
		
		self.price.calcVAT()

class EntryElement(object):
	def __init__(self, description, price):
		self.description = description
		self.price = price

class Task(EntryElement):
	def __init__(self, description, duration, wage, vat):
		super(Task, self).__init__(description, Price(duration * wage, vat))
		self.duration = duration
		self.wage = wage
		
	@staticmethod
	def parseDuration(string, delimiter=':'):
		time = map(lambda x: int(x), string.split(delimiter))
		return(float(time[0] + time[1] / float(60)))
		
	def readableDuration(self, delimiter=':'):
		return str(int(self.duration)) + delimiter + "%02d" % (int((self.duration%1)*60))

class Expenses(EntryElement):
	def __init__(self, description, price, vat):
		super(Expenses, self).__init__(description, Price(price, vat))

class Travel(EntryElement):
	def __init__(self, description, price, vat, fromLocation, toLocation, distance):
		super(Travel, self).__init__(description, Price(price * distance, vat))
		self.fromLocation = fromLocation
		self.toLocation = toLocation
		self.distance = distance
		self.unitPrice = price

class Total(Entry):
	def __init__(self):
		super(Total, self).__init__(Task(None, 0, 0, 0), Expenses(None, 0 , 0), Travel(None, 0, 0, 0, 0, 0))
		self.price = Price()
		
	def update(self, newEntry):
		if newEntry.task:
			self.updateTask(newEntry.task)
		if newEntry.expenses:
			self.updateExpenses(newEntry.expenses)
		if newEntry.travel:
			self.updateTravel(newEntry.travel)
		
	def updateTask(self, task):
		self.updatePrice(self.task.price, task.price)		
		self.task.duration += task.duration
		self.task.wage = self.task.price.subtotal / self.task.duration
		
	def updateExpenses(self, expenses):
		self.updatePrice(self.expenses.price, expenses.price)
		
	def updateTravel(self, travel):
		self.updatePrice(self.travel.price, travel.price)
		self.travel.distance += travel.distance	
		self.task.unitPrice = self.travel.price.subtotal / self.travel.distance

	def updatePrice(self, price, newPrice):
		# Update local price
		price.add(newPrice)		
		# Update global price
		self.price.add(newPrice)
