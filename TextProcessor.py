from Person import Person
from dictGenerator import dictGenerator
#from scheduler import WeeklyScheduler

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
				if(day[0:3].lower() in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]):
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