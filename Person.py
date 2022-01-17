class Person():
	# TODO: Implement an hourly wage and a minimum hours

	def __init__(self, name = "", maxHours = "", availableDays = [], positions = [], weeklyHours = 0):
		self.name = name
		self.maxHours = int(maxHours)
		self.availableDays = availableDays #weekdays
		self.positions = positions
		self.weeklyHours = weeklyHours
		self.workingDays = [] #Add that they can do two shifts in one day???

	def __str__(self):
		return "My name is {} I can work as a(n) {}, I am available on {}, I can work a maximum of {} hours and I am currently scheduled to work {} hours every week".format(self.name, self.positions, self.availableDays, self.maxHours, self.weeklyHours)

	def addHours(self, hours):
		assert self.weeklyHours + hours <= self.maxHours, "This person cannot have that many more hours!"
		self.weeklyHours += hours

	def resetHours(self):
		self.workingDays=[]
		self.weeklyHours = 0

	def addWorkingDay(self, day):
		self.workingDays.append(day)

	def isWorkingOnDay(self, day):
		return day in self.workingDays

	def removeHours(self, hours):
		assert self.weeklyHours - hours >= 0, "This person cannot work a negative amount of hours"
		self.weeklyHours -= hours

	def addAvailability(self, day):
		if(day in self.availableDays):
			print("The employee is already available on {}s".format(day))
		else:
			self.availableDays.append(day)
	def removeAvailability(self, day):
		if(day not in self.availableDays):
			print("The employee does not already have this day set to be available!")
		else:
			self.availableDays.remove(day)

	def setMaxHours(self, maxH):
		self.maxHours = maxH

	def getMaxHours(self):
		return self.maxHours

	def isMaxxedOut(self):
		return self.weeklyHours >= self.getMaxHours()

	def addPositions(self, position):
		if(type(positions)==str):
			self.positions.append(position)
		else:
			self.positions.extend(position)

	def removePositions(self, position):
		print(self.positions)
		if(type(position) == str):
			self.positions.remove(position)
		else:
			for p in position:
				self.positions.remove(p)
		print(self.positions)

	def getPositions(self):
		return self.positions