import threading
import EnergyChannel.Raven as Raven
import EnergyChannel.SQLiteHelper as SQLiteHelper
import EnergyChannel.util as util
import sys

# Modify this to choose where to store the database
DATABASE_FILE = '../ec-channel-ui/ec.db'
ZIPCODE = 92602
SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

class DataDaemon:
	"""
	Multithreading data gathering.
	Storage of misc data is as follows:
	PK    |   KEY    | VALUE
	1     |   Temp   | 54 F
	2     | Location | 1245 Cherry Lane
	"""
	def __init__(self, zipcode):
		self.__raven = Raven()
		self.__db = SQLiteHelper(DATABASE_FILE)
		self.__running = False
		self.__zipcode = zipcode

	def storeRavenData(self):
		try:
			if not self.__raven.exists():
				self.__raven.refresh()
			if self.__running and self.__raven.exists():
				GET_DEMAND = {'Name':'get_instantaneous_demand'}
				self.__raven.write(GET_DEMAND)
				sleep(.05)  
				XMLresponse = self.__raven.read()
				attributes = XMLresponse.getchildren()
				attribute_list = [3,4,5,2]
				# XML frag contains hex, convert to decimal
				data = tuple(int(attributes[i].text, 16) for i in attribute_list)
				self.__db.insert_data(data)
				threading.Timer(7 * SECOND, self.storeRavenData).start()
		except:
			print(sys.exc_info(), file=sys.stderr)

	def storeWeatherData(self):
		try:
			if self.__running:
				temperature = getweather(self.__zipcode)
				self.__db.insertMiscData(1, 'temperature', temperature)
				threading.Timer(1 * HOUR, self.storeWeatherData).start()
		except:
			print(sys.exc_info(), file=sys.stderr)

	def start(self):
		self.__running = True
		self.__storeRavenData()
		self.__storeWeatherData()

	def stop(self):
		self.__running = False

if __name__ == '__main__':
	a = DataDaemon(ZIPCODE)
	a.start()
	input()
	a.stop()
