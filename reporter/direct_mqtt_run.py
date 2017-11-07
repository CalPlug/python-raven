#import threading
import sys
import time
import uuid
import datetime 
import paho.mqtt.client as mqtt
from Raven import Raven


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
		self.mqttc = mqtt.Client("Home_Client")

	def _begin(self):
		self.mqttc.on_message = on_message
		self.mqttc.on_connect = on_connect

		user='xxxxxxxxxxxx'
		password = 'xxxxxxxxxxxxxx'
		port = 17934
		broker_address = 'm10.cloudmqtt.com'

		self.mqttc.username_pw_set(user, password=password)
		self.mqttc.connect(broker_address, port=port)
		self.mqttc.loop_start()
	
	def run(self):
		self._begin()
		while True:
		#	FAKE_DATA = [-1,-1,-1,self.__run, self.__hash]
		#	data=FAKE_DATA
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
						publishTimestamp = now.isoformat()
						attributes = list(XMLresponse)
						attribute_list = [3,4,5]
						# XML frag contains hex, convert to decimal
						data = [int(attributes[i].text, 16) for i in attribute_list]
						data.append(self.__run)
						data.append(self.__hash)
						data.insert(0, str(publishTimestamp))
						data = tuple(data)
						#push to mqtt
						payload = str(data)
						print(payload)
						self.mqttc.publish("test_device/readings", payload=payload)
			

			except:
				self.__raven._raven = None
				self.__raven.refresh() 
			#	print(sys.exc_info(), file=sys.stderr)
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

	RUN_NAME = input('What would you like to title this run? ')
	input('Press enter to begin run.')
	for i in range(3,0,-1):
		print('{}...'.format(i))
		time.sleep(1)
	a = DataDaemon(RUN_NAME)
	a.run()
