"""
Create a weekly schedule for employees based on availability and position

Have flags such as #name #maxhours #availableDays #positions in the input file

Assume that available days are given in weekly format

Needed classes: person, weekly schedule, scheduler, day?

"""

import sys
from Person import Person
from dictGenerator import dictGenerator
from random import randint

class WeeklyScheduler():

	#Daily positions are ones which MUST be filled every day
	#TODO: implement it so that there are time blocks, and specific positions which need to be filled
	#	on specific days

	#For now, assume an eight hour day, where each shift is 8 hours long, improve this later. 

	def __init__(self, skipDays = [], hasWeekends = False, dailyPositions = [], allPositions = [], employees = [], 
		days = ["MON", "TUE", "WED", "THU", "FRI"]):
		self.skipDays = skipDays
		self.dailyPositions = dailyPositions #These need getters and setters and are the positions which MUST be filled everyday
		self.allPositions = allPositions #These need getters and setters
		self.employees = employees
		self.unfilledPositions = []

		self.longest = 0

		self.shiftLength = 8 ##Improve versatily of this later. 

		self.employeesPerPos = {} #Keys are the positions, values are the employees who can work the position
		self.__getPosEmployees()

		self.days = days
		self.schedule={}
		self.removeDays(skipDays)

		for day in self.days:
			self.schedule[day] = {}

		if(hasWeekends):
			self.addWeekends()

	def addEmployee(self, employee):
		self.employees.append(employee)
		self.employeesPerPos={} #See if there's a way to avoid having to reset this list

		self.__getPosEmployees() 

	def addWeekends(self):
		self.addDay("SAT")
		self.addDay("SUN")
		
	def removeWeekends(self):
		self.removeDays(["SAT", "SUN"])

	def getDailyPos(self):
		return self.dailyPositions

	def setDailyPositions(self, dailyPositions):
		print("The daily positions are {}".format(dailyPositions))
		self.dailyPositions=[]
		for position in dailyPositions:
			self.addPosition(position, True)

	def addDailyPosition(self, newDailyPos):
		if(newDailyPos not in self.dailyPositions):
			self.dailyPositions.append(newDailyPos)

	def addPositions(self, newPos):
		for position in newPos:
			self.addPosition(position)

	def addPosition(self, newPosition, isDaily = False):
		if(newPosition not in self.allPositions):
			self.allPositions.append(newPosition)
		if(isDaily):
			self.addDailyPosition(newPosition)

	def setLongestWord(self):
		for position in self.allPositions:
			if(len(position)>self.longest):
				self.longest = len(position)
		for employee in self.employees:
			if(len(employee.name)>self.longest):
				self.longest = len(employee.name)

	def getWeeklySchedule(self):
		return self.schedule

	def getNonDailyPos(self):
		pos = []
		for position in self.allPositions:
			if(position not in self.dailyPositions):
				pos.append(position)

		return pos

	def addDay(self, day):
		if(day.upper() not in self.schedule.keys()):
			self.schedule[day] = {}
			if(day.upper() not in self.days):
				self.days.append(day.upper())
		else:
			print("This day is already in the schedule!")

	def removeDays(self, days):
		for day in days:
			self.removeDay(day)

	def removeDay(self, day):
		print("remove day", day)
		if(day.upper() not in self.days):
			print("This day is not already in the schedule!")
		else:
			self.days.remove(day.upper())
			if(day.upper() in self.schedule.keys()):
				del self.schedule[day.upper()]

	def getUnfilledPositions(self):
		return self.unfilledPositions

	def __fillPos(self, day, posList, offInfo = {}):
		#Offinfo should be a dictionar, employees are keys their values are their off days
		unfilled = []
		offEmps = list(offInfo.keys())
		
		for position in posList:
			chosenIndices = []
			filled=False
			employeesRemain = True
			while (not filled and employeesRemain):
				possibleEmps = self.employeesPerPos[position]
				i = randint(0, len(possibleEmps)-1)
				if(i not in chosenIndices):
					chosenIndices.append(i)
					employee = possibleEmps[i]
					if(not employee.isMaxxedOut()):
						if(not (employee.name in offEmps and day in offInfo[employee.name])):
							if(day in employee.availableDays and not employee.isWorkingOnDay(day)):
								employee.weeklyHours+=self.shiftLength
								employee.workingDays.append(day)
								self.schedule[day][position]=employee.name
								filled=True
					if(len(chosenIndices)==len(possibleEmps)):
						employeesRemain=False
			if(not filled):
				unfilled.append(position)


		return unfilled 

	def resetWeek(self):
		days = list(self.schedule.keys())
		for day in days:
			self.schedule[day] = {}
		for employee in self.employees:
			employee.resetHours()

	def fillDay(self, day, offInfo = {}):
		unfilled = []
		assert day in self.days, "This day is not in the schedule"
		if(day in self.days):
			unfilled = self.__fillPos(day, self.dailyPositions, offInfo)
			unfilled.append(self.__fillPos(day, self.getNonDailyPos(), offInfo))
		return unfilled

	def fillWeek(self, offInfo = {}):
		print("calling from fill week")
		self.removeDays(self.skipDays)
		print("the skips days are", self.skipDays)
		self.resetWeek()
		for day in self.days:
			unfilled = self.fillDay(day, offInfo)
			if(len(unfilled)>0):
				print("Warning! On {} the positions {} are unfilled!".format(day, unfilled))


	def __getPosEmployees(self):
		for position in self.allPositions:
			availableEmps = []
			filled = False
			for employee in self.employees:
				if(position in employee.positions):
					filled = True
					availableEmps.append(employee)
			if(not filled):
				print("unfilled position", position)
				self.unfilledPositions.append(position)
			else:
				self.employeesPerPos[position] = availableEmps

	def printSchedule(self, fileOut = sys.stdout):
		self.setLongestWord()
		dashes = "~"*(len(self.days)*self.longest*2)
		gens = []


		printed = dashes + "\nSchedule\n" + dashes + "\n"

		for day in self.days:
			printed = ("{}{:<" + str(self.longest*2) + "} ").format(printed, day)

		line = ""

		for day in self.days:
			gens.append(dictGenerator(self.schedule[day]))

		continueLooping = True

		dictIndex = 0
		i = 0

		while continueLooping:
			dictIndex=0
			continueLooping=False
			line=""
			for day in self.days:
				info = next(gens[dictIndex])

				a=""
				b=""

				if(info[0]):
					continueLooping = True
					pos = info[1]
					a=pos
					b=self.schedule[day][pos]

				line = ("{}{:<" + str(self.longest) + "}{:<" + str(self.longest) + "} ").format(line,a, b)

				dictIndex+=1

			printed=("{}\n{}".format(printed, line))

		fileOut.write(printed)




class TextProcessor():

	def openFile(self, fileName = "", permission = "r"):
		if(fileName == ""):
			fileName = input("Enter a file name")
		try:
			f = open(fileName, permission)
			return f
		except EOFError:
			print("End of file error when opening file")
			return None
		except FileNotFoundError:
			print("Could not find file {}".format(fileName))
			return None
		except OSError:
			print("Other error")
			return None

	def getNextLine(self, handle = None):
		safe = False
		line = ""

		if(handle is not None):
			try:
				line = handle.readline()
				line = line.strip()
				if(line != ""):
					safe = True
			except EOFError:
				safe = False

		return safe, line


	def getFlagValues(self, flags = [], line = []): #Assume that line is a string list and that no two flag values are occurring simultaneously
		flagValues = {}
		gather = False
		missingFlags = []

		for word in line:
			if(word[0] == "#"):
				flag = word[1:]
				if(flag in flags):
					if(flag not in flagValues.keys()):
						flagValues[flag] = []
					gather = True
				else:
					gather = False
			elif(gather):
				flagValues[flag].append(word)

		for flag in flags:
			if(flag not in flagValues.keys()):
				missingFlags.append(flag)

		if(len(missingFlags)>0):
			print("The flag(s) : {} was(were) not found in the input file".format(" ".join(missingFlags)))

		return flagValues

	def getSkipDays(self, skipDays):
		skips=[]
		if(skipDays!=[]):
			for day in skipDays:
				assert len(day)==3, "Incorrect input, name of day not proper"
				if(day[0:3].lower() in ["mon", "tue", "wed", "thur", "fri", "sat", "sun"]):

					#skips.append(day[0].upper()+day[1:3].lower())
					skips.append(day.upper())
				else:
					warning = "The skip day {} is not in the regular schedule".format(day)
					print(warning)

		return skips

	def getPerson(self, line):
		personInfo = self.getFlagValues(["name", "position", "MaxHours", "AvailableDays"], line)
		assert len(personInfo["MaxHours"]) == 1, "Cannot have more than 1 value for max hours"

		person = Person(name = " ".join(personInfo["name"]), maxHours = personInfo["MaxHours"][0], availableDays = personInfo["AvailableDays"], positions = personInfo["position"])
		return person

	def getScheduleDetails(self, line):
		scheduleInfo = self.getFlagValues(["HasWeekends", "DailyPositions", "SkipDays"], line)

		if("DailyPositions" not in scheduleInfo.keys()):
			scheduleInfo["DailyPositions"] = None
		if("HasWeekends" not in scheduleInfo.keys()):
			scheduleInfo["HasWeekends"] = None 
		if("SkipDays" not in scheduleInfo.keys()):
			scheduleInfo["SkipDays"] = None

		return scheduleInfo

def addScheduleInfo(processor, schedule, line):
	info = processor.getScheduleDetails(line)
	checkScheduleInfo(info, schedule, processor)

def checkScheduleInfo(info, schedule, processor):
	checkDailyPositions(info, schedule)
	checkWeekends(info, schedule)
	checkSkipDays(info, schedule, processor)

def checkDailyPositions(info, schedule):
	if(info["DailyPositions"] is not None):
		schedule.setDailyPositions(info["DailyPositions"])
	else:
		dailyPositions = input("Enter the names of the positions which must be filled daily: ")
		dailyPositions= dailyPositions.split()	
		schedule.setDailyPositions(dailyPositions)	

def checkWeekends(info, schedule):
	if(info["HasWeekends"] is not None):
		weekends = info["HasWeekends"][0].lower() == 'y'
	else:
		weekends = input("Do you want the schedule to have weekends? Enter Y or N: ").lower() == "y"	

	if(weekends):
		schedule.addWeekends()

def checkSkipDays(info, schedule, processor):
	if(info["SkipDays"] is not None):
		schedule.skipDays=info["SkipDays"]
	else:
		skipDays = input("Are there weekdays you want to skip? Enter the first three letters of the weekday(s) or hit Enter for none: ")
		if(skipDays !=""):
			skipDays = list(skipDays.split())
			skipDays = processor.getSkipDays(skipDays)
			schedule.skipDays = skipDays


def addPerson(processor, schedule, line):
		newPerson = processor.getPerson(line)
		
		newPositions = newPerson.getPositions()

		schedule.addPositions(newPositions)

		schedule.addEmployee(newPerson)


def makeSchedule(handle, processor):
	safe, line = processor.getNextLine(handle)

	employees = []
	allPositions=[]
	dailyPositions=[]
	skipDays=[]
	hasWeekends=False
	hasScheduleInfo = False

	schedule = WeeklyScheduler()

	while(safe):
		line = line.split()

		if("#name" in line): #See if there's a better way to flag whether this is person info or not
			addPerson(processor, schedule, line)

		elif("#ScheduleInformation" in line):
			addScheduleInfo(processor, schedule, line)
			hasScheduleInfo= True

		safe, line = processor.getNextLine(handle)

	handle.close()

	if(not hasScheduleInfo):
		info = {"HasWeekends" : None, 
				"DailyPositions" : None,
				"SkipDays" : None	
				}
		checkScheduleInfo(info, schedule, processor)

	schedule.fillWeek()

	schedule.fillWeek({"Regina" : "MON"})
	schedule.printSchedule()



def testing():
	employees = []
	allPos = []

	p = TextProcessor()
	h = p.openFile("testInput")
	safe, line = p.getNextLine(h) #Still have to set it to loop over all the lines

	while(safe):
		line = line.split()
		personInfo = p.getFlagValues(["name", "position", "MaxHours", "AvailableDays"], line)
		assert len(personInfo["MaxHours"]) == 1, "Cannot have more than 1 value for max hours"
		person = Person(name = " ".join(personInfo["name"]), maxHours = personInfo["MaxHours"][0], availableDays = personInfo["AvailableDays"], positions = personInfo["position"])
		employees.append(person)
		safe, line = p.getNextLine(h)

	h.close()

	for person in employees:
		for p in person.positions:
			if(p not in allPos):
				allPos.append(p)

	s = WeeklyScheduler(hasWeekends = True, dailyPositions = ["Human"], allPositions = allPos, employees = employees)
	s.fillWeek()
	s.printSchedule()
	with open("testingOut", "w") as fileOut:
		s.printSchedule(fileOut)

	


def main():
	#testing()

	processor = TextProcessor()
	inFile = input("Please Enter a File Name: ")
	handle = processor.openFile(inFile)

	if(handle is not None):
		makeSchedule(handle, processor)


if __name__ == '__main__':
	main()