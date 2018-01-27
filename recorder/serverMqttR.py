from pymongo import MongoClient
import paho.mqtt.client as mqtt
import re
import datetime
import os
import sys

prev_demand_msg = ''
connected_with_result_code_one = 0
#Improve readability of time

def parse_msg(msg):
	msg = msg.strip('()')
	msg = msg.strip(' ')
	result = msg.split(',')
#	print('Result = ' + str(result))
	cleanResult = []
	for i in result:
		cleanResult.append((i.replace("'", "")).strip(' '))
	print(cleanResult)
	return tuple(cleanResult)

def on_connect(client, userdata, flags, rc):
	global connected_with_result_code_one
	print("Connected with result code " + str(rc))
	connected_with_result_code_one += 1
	if connected_with_result_code_one > 1:
		print("Disconnected -> restarting server...")
		os.execl(sys.executable, 'python', __file__, *sys.argv[1:])

def on_message(client, userdata, msg):

	global prev_demand_msg
	
	demand_msg = str(msg.payload.decode("utf-8"))
	print("Incoming msg payload is :  " + demand_msg)
	if demand_msg == prev_demand_msg:
		return
	else:
		prev_demand_msg = demand_msg
	
	tuple_msg = parse_msg(demand_msg)
	
	client = MongoClient('localhost', 27017)
	db = client.pulses
	test_readings = db.InstantaneousDemandTest1
	test_readings_data = {
		'time':		 	 tuple_msg[0],
		'utcTime':       datetime.datetime.utcnow(),
		'MeterID':	 	 tuple_msg[1],
		'demand': 		 tuple_msg[2],
		'run':			 tuple_msg[3],
		'hash':			 tuple_msg[4],
		'summationDelivered':	 tuple_msg[5],
		'summationReceived':	 tuple_msg[6]
		
	}
	result = test_readings.insert_one(test_readings_data)
	#Uncomment to test
	print('One post: {0}'.format(result.inserted_id))
	
if __name__ =='__main__':
	mqttc = mqtt.Client("Calit2_Server1")
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect

	user = 'dkpljrty'
	password = 'ZJDsxMVKRjoR'
	port = 17934
	broker_address = 'm10.cloudmqtt.com'

	mqttc.username_pw_set(user, password=password)
	mqttc.connect(broker_address, port=port)
	mqttc.subscribe("test_device/readingsTest")
	mqttc.loop_forever()

