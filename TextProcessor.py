from Person import Person
from dictGenerator import dictGenerator


class TextProcessor():
	"""A class meant to process and extract information from an input file for a scheduler"""

	def openFile(self, fileName = "", permission = "r"):
		"""Open a file with a given name and permission

			Arguments: fileName (string) : Name of file to open
					   permission (string) : permission to open file with
			Returns: Handle of opened file, if opening was successful
		"""

		#Attempt to open the file with the given name, catch and print any errors
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
		"""Get the next line from a file

		Arguments: handle (file handle) : Handle of file to get the next line from
		Returns: safe (boolean) : A flag indicating if there was a line found in the file
				 line (string) : The next line found in the file
		"""

		#Assumed unsafe input and a blank line
		safe = False
		line = ""

		#Get the next line from the input file if the handle is valid
		if(handle is not None):
			try:
				line = handle.readline()
				line = line.strip()

				#Check if the line was empty or if the end of the file has been reached
				if(line != ""):
					safe = True
			except EOFError:
				safe = False

		return safe, line


	def getFlagValues(self, flags = [], line = []): #Assume that line is a string list and that no two flag values are occurring simultaneously
		"""Get values flagged in a file
		Arguments: flags (string list) : list of flags to be looking for
				   line (string list) : list of a split string of input
		Returns: flagValues (dictionary) : Keys are the flags, values are the information found for those flags
		"""

		flagValues = {}
		#Gather indicates if the processor should be treating the current string element as information or not
		gather = False
		missingFlags = []

		#Iterate through each word in the line list
		for word in line:

			#Any word starting with # is a flag name
			if(word[0] == "#"):
				flag = word[1:]
				if(flag in flags):
					if(flag not in flagValues.keys()):
						flagValues[flag] = []

					#If a flag is encountered, gather all string elements between itself and the next flag as information
					#for that flag in particular
					gather = True
				else:
					#If this flag isn't in the list of flags to be looked for, don't gather the information between itself
					#and the next flag
					gather = False
			elif(gather):
				#All elements between desired flags should be treated as information for the previous flag
				flagValues[flag].append(word)

		for flag in flags:
			#Check for flags that were arguments but not found
			if(flag not in flagValues.keys()):
				missingFlags.append(flag)

		#Alert the user about any missing flags
		if(len(missingFlags)>0):
			print("The flag(s) : {} was(were) not found in the input file".format(" ".join(missingFlags)))

		return flagValues

	def getSkipDays(self, skipDays):
		"""
		Check that a skip day is in the file

		Arguments: skipDays (stirng list) : list of days wanting to be skipped
		Returns: skips (string list) : list of days which were successfully set to be skipped
		"""

		skips=[]
		if(skipDays!=[]):
			for day in skipDays:

				#Check that the day name was inputted properly
				assert len(day)==3, "Incorrect input, name of day not proper"

				#Check that the day exists in the default list of schedule days
				if(day[0:3].lower() in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]):
					#If it is a default day, append it to the list of days to be skipped
					skips.append(day.upper())
				else:
					#Warn the user if the skip day was not on the regular schedule
					warning = "The skip day {} is not in the regular schedule".format(day)
					print(warning)

		return skips

	def getPerson(self, line):
		"""
		Extract a person's information from a text line

		Arguments: line (string) : line to extract information from
		Returns: person (Person) : A person object with the extracted information
		"""

		#Get the information which should be stored in flag values
		personInfo = self.getFlagValues(["name", "position", "MaxHours", "AvailableDays"], line)

		#Assert that the maxhours was formatted properly in the input file
		assert len(personInfo["MaxHours"]) == 1, "Cannot have more than 1 value for max hours"

		#Create a Person object with the extracted information
		person = Person(name = " ".join(personInfo["name"]), maxHours = personInfo["MaxHours"][0], availableDays = personInfo["AvailableDays"], positions = personInfo["position"])
		
		return person

	def getScheduleDetails(self, line):
		"""Extract information about the schedule from an input line

		Arguments: line (string) : A line of information from an input file
		Returns: scheduleInfo (dictionary) : The keys are the field names and the values are the information for that field
		"""

		#Get the schedule information that should be in the line
		scheduleInfo = self.getFlagValues(["HasWeekends", "DailyPositions", "SkipDays"], line)

		#Check that the desired information was in the line, and if not, still create a key for them with a None value
		if("DailyPositions" not in scheduleInfo.keys()):
			scheduleInfo["DailyPositions"] = None
		if("HasWeekends" not in scheduleInfo.keys()):
			scheduleInfo["HasWeekends"] = None 
		if("SkipDays" not in scheduleInfo.keys()):
			scheduleInfo["SkipDays"] = None

		return scheduleInfo