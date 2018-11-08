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
RESTART_RAVEN = {'Name':'restart'}

class DataDaemon:
	"""
	#Multithreading data gathering.
	Single-threaded for now, issues with multithreading.
	"""
	def __init__(self, run):
		self.__run = run
		self.__hash = str(uuid.uuid4())
		self.__raven = Raven()
		self.__mqttc = mqtt.Client("Lab_Client1")
	def _begin(self):
		
		self.__raven.write(RESTART_RAVEN)  #test
		
		self.__mqttc.on_message = on_message
		self.__mqttc.on_connect = on_connect

		user='dkpljrty'
		password = 'ZJDsxMVKRjoR'
		port = 17934
		broker_address = 'm10.cloudmqtt.com'

		self.__mqttc.username_pw_set(user, password=password)
		self.__mqttc.connect(broker_address, port=port)
		self.__mqttc.loop_start()
	
	def run(self):
		
		self._begin()
		summation_data = []
		prev_xml_tag = ''

		while True:
	#		FAKE_DATA = [-1,-1,-1,self.__run, self.__hash, -1, -1, -1, -1]
	#		data=FAKE_DATA
			try:
				if not self.__raven.exists(): 
					print("searching...")
					self.__raven.refresh()
				if self.__raven.exists():
					GET_CURRENT_SUMMATION_DELIVERED = {'Name':'get_current_summation_delivered'}
					self.__raven.write(GET_CURRENT_SUMMATION_DELIVERED)
					time.sleep(.1) 
			
					XMLresponse = self.__raven.read()
					if (XMLresponse.tag == 'InstantaneousDemand'):
						final_data_to_push = []
						temp_data = []
						now = datetime.datetime.now()
						publishTimestamp = now.isoformat()
						attributes = list(XMLresponse)
						attribute_list = [1,3,4,5]
						# XML frag contains hex, convert to decimal
						
						temp_data = [int(attributes[i].text, 16) for i in attribute_list]
						final_data_to_push.append(temp_data[0]) #MeterID
						demand_multiplier = temp_data[2] if temp_data[2] != 0 else 1
						demand_divisor = temp_data[3] if temp_data[3] != 0 else 1
						final_data_to_push.append(temp_data[1] * demand_multiplier / float(demand_divisor)) #Demand
						final_data_to_push.append(self.__run)
						final_data_to_push.append(self.__hash)
						final_data_to_push.insert(0, str(publishTimestamp))
						
						if(prev_xml_tag == 'CurrentSummationDelivered'):
							summation_multiplier = summation_data[5] if summation_data[5] != 0 else 1
							summation_divisor = summation_data[6] if summation_data[6] != 0 else 1
							final_data_to_push.append(summation_data[3] * summation_multiplier / float(summation_divisor))   #SummationDelivered
							final_data_to_push.append(summation_data[4] * summation_multiplier / float(summation_divisor))   #SummationRecieved
							prev_xml_tag = 'InstantaneousDemand'
							summation_data = []
						else:
							final_data_to_push.append('')
							final_data_to_push.append('')
						#push to mqtt
						payload = str(final_data_to_push)
						print(payload)
						self.__mqttc.publish("test_device/readingsTest", payload=payload[1:-1]) #change to test_device/readings to record
						data = []
					elif(XMLresponse.tag == 'CurrentSummationDelivered'):
			
						prev_xml_tag = XMLresponse.tag
						attributes = list(XMLresponse)
						# XML frag contains hex, convert to decimal
						for i in attributes:
							summation_data.append(int(i.text, 16))

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
	if (len(sys.argv) > 1):
		if sys.argv[1] == '-usemac':
			RUN_NAME = str(hex(uuid.getnode()))
			print(RUN_NAME)
		elif sys.argv[1] == '-username':
			RUN_NAME = sys.argv[2] # Title of run via cli (-username UserNameHere)
	else:
		RUN_NAME = input('What would you like to title this run? ')
		input('Press enter to begin run.')
	for i in range(3,0,-1):
		print('{}...'.format(i))
		time.sleep(1)
	a = DataDaemon(RUN_NAME)
	a.run()
