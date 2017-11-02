#import threading
import sys
import time
import uuid
import datetime 
import paho.mqtt.client as mqtt

from Raven import Raven
#from MySQLHelper import MySQLHelper

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

'''Note: We should be changing this to be threaded shortly after getting the single threaded version working'''
class DataDaemon:
	"""
	#Multithreading data gathering.
	Single-threaded for now, issues with multithreading.
	"""
	def __init__(self, run):
		self.__run = run
		self.__hash = str(uuid.uuid4())
		self.__raven = Raven()
	#	self.__db = MySQLHelper()

	def _begin(self):
		#self.__db.insertRunInfo([self.__hash,self.__run])
		mqttc = mqtt.Client("Home_Client")
		mqttc.on_message = on_message
		mqttc.on_connect = on_connect

		user='dkpljrty'
		password = 'ZJDsxMVKRjoR'
		port = 17934
		broker_address = 'm10.cloudmqtt.com'

		mqttc.username_pw_set(user, password=password)
		mqttc.connect(broker_address, port=port)
		mqttc.loop_start()
	
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
						now = datetime.datetime.now()
						publishTimestamp = now.isoformat(timespec = 'seconds')
						attributes = list(XMLresponse)
						attribute_list = [3,4,5]
						# XML frag contains hex, convert to decimal
						data = [int(attributes[i].text, 16) for i in attribute_list]
						data.append(self.__run)
						data.append(self.__hash)
						data.insert(0, publishTimestamp)
						data = tuple(data)
						#data += (self.__run,self.__hash)
					print(data)
					'''serverside script must be altered to deal with the format of data'''
				#	self.__db.insertDemandData(data) #no longer needed
					'''push to mqtt'''
					payload = str(data)
					mqttc.publish("test_device/readings", payload=payload)

			except:
				self.__raven._raven = None
				self.__raven.refresh()
				data = FAKE_DATA
				#self.__db.insertDemandData(data)
				print(sys.exc_info(), file=sys.stderr)
			time.sleep(8)

	#Callbacks
	def on_connect(client, userdata, flags, rc):

		print("Connected with result code " + str(rc))

	def on_message(client, userdata, msg):

		print("message received ", str(msg.payload.decode("utf-8")))
		print("message topic=", msg.topic)
		print("message qos=", msg.qos)
		print("message retain flag=", msg.retain)


if __name__ == '__main__':
	'''connect to mqtt'''
	RUN_NAME = input('What would you like to title this run? ')
	input('Press enter to begin run.')
	for i in range(3,0,-1):
		print('{}...'.format(i))
		time.sleep(1)
	a = DataDaemon(RUN_NAME)
	a.run()
