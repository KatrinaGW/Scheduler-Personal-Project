def dictGenerator(dictionary):
		i = 0
		length = len(dictionary.keys())
		k = list(dictionary.keys())

		while True:
			if(i>=length):
				yield False, ""
			else:
				yield True, k[i]

			i+=1

