

class echo():
	def __init__(self, fileName):
		self.fileName = fileName

	def writeConfig(self, configDict):
		keys = list(configDict.keys())

		configToWrite = []

		for index, key in enumerate(keys):
			if index == 0:
				string = """echo {"'%s'": "'%s'",  >> %s""" % (key, configDict[key], self.fileName)
			elif index == len(keys) - 1:
				string = """echo "'%s'": "'%s'"}  > %s""" % (key, configDict[key], self.fileName)
			else:
				string = """echo "'%s'": "'%s'",  > %s""" % (key, configDict[key], self.fileName)

			configToWrite.append(string)

		return configToWrite
