#import threading
import sys
import time
import uuid

from Raven import Raven
from MySQLHelper import MySQLHelper

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

class DataDaemon:
	"""
	#Multithreading data gathering.
	Single-threaded for now, issues with multithreading.
	"""
	def __init__(self, run):
		self.__run = run
		self.__hash = str(uuid.uuid4())
		self.__raven = Raven()
		self.__db = MySQLHelper()

	def _begin(self):
		self.__db.insertRunInfo([self.__hash,self.__run])

	def run(self):
		self._begin()
		FAKE_DATA = (-1,-1,-1,self.__run, self.__hash)
		while True:
			data=FAKE_DATA
			try:
				if not self.__raven.exists():
					print("searching...")
					self.__raven.refresh()
				if self.__raven.exists():
					GET_DEMAND = {'Name':'get_instantaneous_demand'}
					self.__raven.write(GET_DEMAND)
					time.sleep(.1)  
					XMLresponse = self.__raven.read()
					if (XMLresponse.tag == 'InstantaneousDemand'):
						attributes = list(XMLresponse)
						attribute_list = [3,4,5]
						# XML frag contains hex, convert to decimal
						data = tuple(int(attributes[i].text, 16) for i in attribute_list)
						data += (self.__run,self.__hash)
					print(data)
					self.__db.insertDemandData(data)
			except:
				self.__raven._raven = None
				self.__raven.refresh()
				data = FAKE_DATA
				self.__db.insertDemandData(data)
				print(sys.exc_info(), file=sys.stderr)
			time.sleep(8)

if __name__ == '__main__':
	RUN_NAME = input('What would you like to title this run? ')
	input('Press enter to begin run.')
	for i in range(3,0,-1):
		print('{}...'.format(i))
		time.sleep(1)
	a = DataDaemon(RUN_NAME)
	a.run()
