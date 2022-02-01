"""

Please note that this project is an ongoing work in progress. 

"""

import sys
from Person import Person
from dictGenerator import dictGenerator
from random import randint
from TextProcessor import TextProcessor

class WeeklyScheduler():
	#Class WeeklyScheduler creates a weekly schedule for employees who work shifts. There are different
	#settings and options depending on what the employer wants. 

	#TODO: implement it so that there are time blocks, and specific positions which need to be filled
	#	on specific days
	#TODO: Make it so that it shifts don't have to be 8 hours. 

	def __init__(self, skipDays = [], hasWeekends = False, dailyPositions = [], allPositions = [], employees = [], 
		days = ["MON", "TUE", "WED", "THU", "FRI"]):
		""" Constructs a WeeklyScheduler object

			Arguments:
				skipDays (string list) : A list of days not to include in the weekly schedule
				hasWeekends (boolean) : A boolean value indicating if weekends should be included on 
										the schedule
				dailyPositions (string list) : A list of positions which must be filled everyday
				allPositions (string list) : A list of all the positions possible
				employees (Person list) : A list of all the employees to schedule
				days (string list) : A list of all the days in the week

			Returns: None
		"""

		#Initialize the instance variables to be the values passed in as arguments
		self.skipDays = skipDays
		self.dailyPositions = dailyPositions 
		self.allPositions = allPositions 
		self.employees = employees

		#List of positions which go unfilled after making the schedule
		self.unfilledPositions = []

		#The length of the longest word on the schedule, used to format printing
		self.longest = 0

		#Length of a shift, this will be made more versatile later. 
		self.shiftLength = 8

		#Dictionary where the positions are the keys, and the employees who can work those positions are the values
		self.employeesPerPos = {} 

		#Fill the employeesPerPos dictionary
		self.__getPosEmployees()

		self.days = days

		#Create an empty dictionary for the weekly schedule. Keys will be the days, values will be the positions
		#and the employees working them
		self.schedule={}

		#Remove the skip days from the schedule
		self.removeDays(skipDays)

		#Create an empty schedule for each day in the week, keys will be the positions, and the value will be 
		#the employee working that position, that day
		for day in self.days:
			self.schedule[day] = {}

		if(hasWeekends):
			self.addWeekends()

	def addEmployee(self, employee):
		"""
		Adds an employee to the schedule

		Arguments: employee (Person) : The employee to be added to the schedule
		Returns: None
		"""

		#Add the new employee to the employee list
		self.employees.append(employee)

		#Reset the employees per position list, then make it again with the new employee
		self.employeesPerPos={}
		self.__getPosEmployees() 

	def addWeekends(self):
		"""
		Add weekends to the schedule

		Arguments: None
		Returns: None
		"""

		#Add saturday and sunday to the days on the schedule
		self.addDay("SAT")
		self.addDay("SUN")
		
	def removeWeekends(self):
		"""
		Removes weekends from the schedule

		Arguments: None
		Returns: None
		"""

		#Remove saturday and sunday from the schedule
		self.removeDays(["SAT", "SUN"])

	def getDailyPos(self):
		"""
		Gets the positions which must be filled daily

		Arguments: None
		Returns: This list of daily positions
		"""

		return self.dailyPositions

	def setDailyPositions(self, dailyPositions):
		"""
		Set the daily positions

		Arguments: dailyPositions (string list) : List of the names of positions
					which must be filled daily
		Returns: None
		"""

		#Reset the current daily position list
		self.dailyPositions=[]

		#Add each position in the new daily position list
		for position in dailyPositions:
			self.addPosition(position, True)

	def addDailyPosition(self, newDailyPos):
		"""
		Add a daily position

		Arguments: newDailyPos (string) : Name of daily position to be added
		Returns: None
		"""

		#If the daily position is not already in the daily position list, add it
		if(newDailyPos not in self.dailyPositions):
			self.dailyPositions.append(newDailyPos)

	def addPositions(self, newPos):
		"""
		Adds new positions to the schedule

		Arguments: newPos (string list) : list of positions to add to the schedule
		Returns: None
		"""

		#For each position in the new position list, add it to the scheduler's positions
		for position in newPos:
			self.addPosition(position)

	def addPosition(self, newPosition, isDaily = False):
		""" 
		Add a new position to the scheduler

		Arguments: newPosition (String) : name of position to add to the scheduler
				   isDaily (boolean) : a boolean flag indicating whether or not this position is daily

		Returns: None
		"""

		#If the position is not already in the schedule, append it
		if(newPosition not in self.allPositions):
			self.allPositions.append(newPosition)
		#If this position is daily, add it to the daily position list
		if(isDaily):
			self.addDailyPosition(newPosition)

	def setLongestWord(self):
		"""
		Set the longest word in the schedule

		Arguments: None
		Returns: None
		"""

		#Find the longest position name
		for position in self.allPositions:
			#If the longest position name is longer than the current longest word in the schedule,
			#set it to be the new longest word in the schedule
			if(len(position)>self.longest):
				self.longest = len(position)
		#Find the longest employee name
		for employee in self.employees:
			#If the longest employee name is longer than the current longest word in the schedule, set
			#it to be the new longest word inthe schedule
			if(len(employee.name)>self.longest):
				self.longest = len(employee.name)

	def getWeeklySchedule(self):
		"""
		Get the weekly schedule

		Arguments:None
		Returns: schedule (dictionary) : The weekly schedule where the keys are the days, the values are dictionaries
											where the keys are positions and the values are the employees working
											that position
		"""

		return self.schedule

	def getNonDailyPos(self):
		"""
		Get the positions which are not daily

		Arguments: None
		Returns: pos (string list) : list of positions which do not have to be filled daily
		"""

		pos = []

		#If a position in the schedule's position list is not in its daily position list, append it
		#to the list of non daily positions
		for position in self.allPositions:
			if(position not in self.dailyPositions):
				pos.append(position)

		return pos

	def addDay(self, day):
		"""
		Add a day to the schedule

		Arguments: day (string) : the day to be added to the schedule
		Returns: None
		"""

		#If the day is not already in the schedule, add it as a new key in the schedule dictionary
		if(day.upper() not in self.schedule.keys()):
			self.schedule[day] = {}

			#If the day is not already in the separate day list, append it to the list
			if(day.upper() not in self.days):
				self.days.append(day.upper())
		else:
			#Inform the user that this day was already in the schedule
			print("This day is already in the schedule!")

	def removeDays(self, days):
		"""
		Remove days from the schedule

		Arguments: days (string list) : names of days to be removed from the schedule
		Returns: None
		"""

		#Remove each day in the list of days to be removed
		for day in days:
			self.removeDay(day)

	def removeDay(self, day):
		"""
		Remove a day from the schedule

		Arguments : day (string) : name of the day to remove from the schedule
		Returns: None
		"""

		#Check that the day is actually in the schedule
		if(day.upper() not in self.days):
			#Warn the user that this day isn't in the schedule
			print("This day is not already in the schedule!")
		else:
			#First remove the day from the list of days in the schedule, then remove its
			#key value pair from the schedule dictionary
			self.days.remove(day.upper())
			if(day.upper() in self.schedule.keys()):
				del self.schedule[day.upper()]

	def getUnfilledPositions(self):
		"""
		Get the list of positions which were unfilled

		Arguments: None
		Returns: unfilledPositions (string list) : list of positions that were unfilled
		"""

		return self.unfilledPositions

	def __fillPos(self, day, posList, offInfo = {}):
		"""
		Fill a position

		Arguments: day (string) : name of day this position is being filled for
				   posList (string list) : Names of positions to be filled this day
				   offInfo (dictionary) : Employees with off days are the keys, the days they're off
				   							are the values
		Returns: unfilled (string list) : list of positions which could not be filled this day
		"""
		#Create a list for the unfilled positions, and the employees who are off
		unfilled = []
		offEmps = list(offInfo.keys())
		
		for position in posList:

			#Indices of employees which the scheduler has already tried to schedule for this
			#day and position
			chosenIndices = []

			#Indicates whether or not the position is filled
			filled=False

			#Indicates if there are still employees to try filling the position with
			employeesRemain = True

			while (not filled and employeesRemain):

				#Get the employees who can work this position
				possibleEmps = self.employeesPerPos[position]

				#Randomly select an indice to try to avoid always having the same employee work the
				#same position every day
				i = randint(0, len(possibleEmps)-1)

				#Try filling the position with a new employee
				if(i not in chosenIndices):
					chosenIndices.append(i)
					employee = possibleEmps[i]

					#If the employee hasn't maxxed out their hours and isn't schedule to be off, schedule
					#them to work this position on this day
					if(not employee.isMaxxedOut()):
						if(not (employee.name in offEmps and day in offInfo[employee.name])):
							if(day in employee.availableDays and not employee.isWorkingOnDay(day)):
								#add to their hours worked this week
								employee.weeklyHours+=self.shiftLength

								#Schedule the employee to work this position on this day
								employee.workingDays.append(day)
								self.schedule[day][position]=employee.name
								filled=True

					#Check that there are still employees who might be able to work this position on this day
					if(len(chosenIndices)==len(possibleEmps)):
						employeesRemain=False

			#If add to unfilled positions if no employee was able to work the position this day
			if(not filled):
				unfilled.append(position)

		return unfilled 

	def resetWeek(self):
		"""
		Unfill all the positions for this week

		Arguments: None
		Returns: None
		"""

		days = list(self.schedule.keys())

		#Clear the positions from each day in the schedule
		for day in days:
			self.schedule[day] = {}

		#Reset all employees to have worked no shifts this week
		for employee in self.employees:
			employee.resetHours()

	def fillDay(self, day, offInfo = {}):
		"""
		Fill a day in the schedule

		Arguments: day (string): Name of day to be filled
				   offInfo (dictionary): Employees are keys, values are the days that they cannot work this week, apart
				   							from their usual non scheduled days
		Returns: unfilled (string list) : List of positions which could not be filled
		"""

		unfilled = []

		#Assert that this day is actually in the schedule
		assert day in self.days, "This day is not in the schedule"

		#First fill the daily positions then fill the non daily positions. Both will return a list
		#of positions which could not be filled
		if(day in self.days):
			unfilled = self.__fillPos(day, self.dailyPositions, offInfo)
			unfilled.append(self.__fillPos(day, self.getNonDailyPos(), offInfo))

		#Return all the positions which could not be filled
		return unfilled

	def fillWeek(self, offInfo = {}, giveWarning = True):
		"""
		Fill the schedule for the week

		Arguments: offInfo (dictionary): Employees are keys, values are the days that they cannot work this week, apart
				   							from their usual non scheduled days
				   giveWarning (boolean) : Indicates whether or not the user wants to be informed about positions
				   							which went unfilled
		Returns: None
		"""

		#First remove the days specified to be skipped
		self.removeDays(self.skipDays)

		#Reset the current weekly schedule
		self.resetWeek()

		#Fill each day in the week
		for day in self.days:
			unfilled = self.fillDay(day, offInfo)

			#If the user wants, alert them about unfilled positions
			if(len(unfilled)>0 and giveWarning):
				print("Warning! On {} the positions {} are unfilled!".format(day, unfilled))


	def __getPosEmployees(self):
		"""
		Get the employees who can work each position

		Arguments: None
		Returns: None
		"""

		#For each position, get the employees who can work that position
		for position in self.allPositions:
			availableEmps = []
			filled = False

			#If an employee can work that position, add them to the list of employees who can work it
			for employee in self.employees:
				if(position in employee.positions):
					filled = True
					availableEmps.append(employee)
			if(not filled):
				self.unfilledPositions.append(position)
			else:
				#Set the values of this position to be the employees who can work it
				self.employeesPerPos[position] = availableEmps

	def printSchedule(self, fileOut = sys.stdout):
		"""
		Print the current weekly schedule

		Arguments: fileOut (file handle) : Handle of file to print the schedule to
		Returns: None
		"""

		#Use the longest word to scale how large each column should be
		self.setLongestWord()
		dashes = "~"*(len(self.days)*self.longest*2)

		#Create a list of generators for each day's dictionary in the schedule
		gens = []

		#Get a header for the dictionary
		printed = dashes + "\nSchedule\n" + dashes + "\n"

		#Add the string for each day name to the schedule
		for day in self.days:
			printed = ("{}{:<" + str(self.longest*2) + "} ").format(printed, day)

		line = ""

		#Create a generator for each day dictionary in the schedule
		for day in self.days:
			gens.append(dictGenerator(self.schedule[day]))

		continueLooping = True

		#Create an index to keep track of which day's dictionary is currently being accessed
		dictIndex = 0

		i = 0

		#Continue looping until no days have any positions left to add to the printed schedule
		while continueLooping:
			dictIndex=0
			continueLooping=False
			line=""
			for day in self.days:
				#Get the next position and employee working it from the day's dictionary
				info = next(gens[dictIndex])

				#a is the position name, b is the employee scheduled to work that position, on that day
				a=""
				b=""

				#The first element in the day's info indicates if there was a position returned for that day, and if there
				#was, to print it on the day's column
				if(info[0]):
					continueLooping = True

					#Get the position and the employee working it on that day
					pos = info[1]
					a=pos
					b=self.schedule[day][pos]

				#Add that employee and position to the current line, in the column for the current day
				line = ("{}{:<" + str(self.longest) + "}{:<" + str(self.longest) + "} ").format(line,a, b)

				#Move down a line after all the days have been searched for a next position
				dictIndex+=1

			#Add the filled line to the line to be printed, then move down a line
			printed=("{}\n{}".format(printed, line))

		#Print the schedule to the desired output file
		fileOut.write(printed)

		fileOut.close()

def addScheduleInfo(processor, schedule, line):
	"""
	Add a line of information from an input file, to a scheduler

	Arguments: processor (TextProcessor) : The processor being used to process the input file
			   schedule (WeeklyScheduler) : scheduler to add the information to
			   line (string) : line of information from an input file
	Returns: None
	"""

	#Extract information for the schedule from the current line of input
	info = processor.getScheduleDetails(line)

	#Check the extracted information to see how to add it to the scheduler
	checkScheduleInfo(info, schedule, processor)

def checkScheduleInfo(info, schedule, processor):
	"""
	Check for fields and extract their information for the scheduler

	Arguments: info (dictionary) : keys are field names, values are the information in those fields
	Returns: None
	"""

	#Check if the information pertains to daily positions, weekends, or skipdays
	checkDailyPositions(info, schedule)
	checkWeekends(info, schedule)
	checkSkipDays(info, schedule, processor)

def checkDailyPositions(info, schedule):
	"""
	Check if there is information about the scheduler's  daily positions

	Arguments: info (dictionary) : keys are field names, values are the information in those fields
			   scheduler (WeeklyScheduler) : The current scheduler to add any information to
	Returns: None
	"""

	#If there is information about the daily positions, add it to the scheduler
	if(info["DailyPositions"] is not None):
		schedule.setDailyPositions(info["DailyPositions"])
	else:
		#Get information about the daily positions from the user, and that information to the scheduler
		dailyPositions = input("Enter the names of the positions which must be filled daily: ")
		dailyPositions= dailyPositions.split()	
		schedule.setDailyPositions(dailyPositions)	

def checkWeekends(info, schedule):
	"""
	Check if there is information about the scheduler's weekends 

	Arguments: info (dictionary) : keys are field names, values are the information in those fields
			   scheduler (WeeklyScheduler) : The current scheduler to add any information to
	Returns: None
	"""

	#If there was information about it, see if the hasWeekends value was affirmative
	if(info["HasWeekends"] is not None):
		weekends = info["HasWeekends"][0].lower() == 'y'
	else:
		#Ask the user if they want weekends on the schedule
		weekends = input("Do you want the schedule to have weekends? Enter Y or N: ").lower() == "y"	

	#If indicated, add weekends to the schedule
	if(weekends):
		schedule.addWeekends()

def checkSkipDays(info, schedule, processor):
	"""
	Check if there is information about the scheduler's skip days

	Arguments: info (dictionary) : keys are field names, values are the information in those fields
			   scheduler (WeeklyScheduler) : The current scheduler to add any information to
	Returns: None
	"""

	#If there is information about them, add the skip days to the scheduler
	if(info["SkipDays"] is not None):
		schedule.skipDays=info["SkipDays"]
	else:
		#Ask the user for information about the days to skip, and add it to the scheduler
		skipDays = input("Are there weekdays you want to skip? Enter the first three letters of the weekday(s) or hit Enter for none: ")
		if(skipDays !=""):
			skipDays = list(skipDays.split())
			skipDays = processor.getSkipDays(skipDays)
			schedule.skipDays = skipDays


def addPerson(processor, schedule, line):
	"""
	Add an employee and their information to the scheduler

	Arguments: processor (TextProcessor) : The current processor being used for the input file
			   schedule (WeeklyScheduler) : The scheduler to add an employee to
			   line (string) : The current line of input from the input file
	Returns: None
	"""

	#Get an employee's information from the line of input, and add it to the scheduler
	newPerson = processor.getPerson(line)
		
	newPositions = newPerson.getPositions()

	schedule.addPositions(newPositions)

	schedule.addEmployee(newPerson)

def giveWarning():
	"""
	See if user wants warnings about unfilled positions

	Arguments: None
	Returns: wantsWarning (boolean) : A flag indicating if the user wants the warnings or not
	"""

	decision = input("Do you want a warning about which positions are unfilled each day? Enter Y or N : ")

	#The user wants a warning if they entered a y
	wantsWarning = decision.lower()=="y";

	return wantsWarning;


def makeSchedule(iHandle, oHandle, processor):
	"""
	Make a weekly schedule for employees

	Arguments: iHandle (file handle) : The handle for the input file
			   oHandle (file handle) : The handle for the output file
			   processor (TextProcessor) : The processor to use to process the input file for schedule information
	Returns: None
	"""

	safe, line = processor.getNextLine(iHandle)

	#Initialize a variable to indicate if the input file had information about the schedule or not
	hasScheduleInfo = False

	schedule = WeeklyScheduler()

	#While there are still lines in the input file, check if each one has information about an employee or about
	#the schedule
	while(safe):
		line = line.split()

		#If there is a field called "name" this is a line with person information
		if("#name" in line):
			addPerson(processor, schedule, line)

		#ScheduleInformation is a flag that this line has information aobut the schedule
		elif("#ScheduleInformation" in line):
			addScheduleInfo(processor, schedule, line)
			hasScheduleInfo= True

		safe, line = processor.getNextLine(iHandle)

	iHandle.close()

	#If the input file did not have schedule information, ask the user to fill in that information
	if(not hasScheduleInfo):
		info = {"HasWeekends" : None, 
				"DailyPositions" : None,
				"SkipDays" : None	
				}

		checkScheduleInfo(info, schedule, processor)

	schedule.fillWeek(giveWarning= giveWarning())
	"""TODO: Get the offinfo from the input. To see how the off info works, uncomment the following
	         line of code and comment out the previous one when using either of the provided test input files """
	#schedule.fillWeek(offInfo = {"Regina" : "MON"} giveWarning = giveWarning())

	#Print the schedule to the provided output file, and if it wasn't the standard output, let the user know
	#that it printed successfully
	schedule.printSchedule(oHandle)
	if(oHandle != sys.stdout):
		print("Schedule has successfully been printed to output file")

def main():

	#Create a processor for the input file
	processor = TextProcessor()

	#Get an input file and create its handle
	inFile = input("Please Enter an Input File Name: ")
	iHandle = processor.openFile(inFile, "r")

	#Get an output file and create its handle
	outFile = input("Please Enter the Output File Name or Hit Enter to Print the Schedule to the Standard Output: ")
	if(outFile == ""):
		oHandle = sys.stdout
	else:
		oHandle = processor.openFile(outFile, "w")

		#If the processor failed to open the output file, default to the standard output
		if(oHandle is None):
			oHandle = sys.stdout
			print("Schedule will be Printed to Standard Output")


	#If a valid input handle was created, create the schedule
	if(iHandle is not None):
		makeSchedule(iHandle, oHandle, processor)


if __name__ == '__main__':
	main()
