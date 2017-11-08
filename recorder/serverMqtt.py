from pymongo import MongoClient
import paho.mqtt.client as mqtt
import re
import datetime

prev_demand_msg = ''

#Format of incoming str
'''(datetime.datetime(2016, 10, 20, 13, 3, 1), -1, -1, -1, 'Test', '')'''

#Improve readability of time
def parse_time(result) -> str:
	date_time = '<'
	for i in range(0, 3):
		unit_of_time = re.sub('[^0-9]', '',result[i])
		if(len(unit_of_time) == 1):
			unit_of_time = '0' + unit_of_time
		date_time += unit_of_time
		if i != 2:
			date_time += '-'
	date_time += 'T'
	for i in range(3,6):
		unit_of_time = re.sub('[^0-9]', '',result[i])
		if(len(unit_of_time) == 1):
			unit_of_time= '0' + unit_of_time
		date_time += unit_of_time
		if i != 5:
			date_time += ':'
	date_time += '>'
	return date_time

def parse_msg(msg) -> tuple:
	result = msg.split()
	result_list = list()
	date_time = parse_time(result)
	result_list.append(date_time)

	run = '-1'
	hashID = '-1'
	print(result)
	print(len(result))
	if len(result) > 6:
		for i in range(6,9):
			res = re.sub('[^-\d]', '', result[i])
			result_list.append(res)
		run = re.sub('[^A-Z | ^a-z]','',result[9])
		hashID = re.sub('[^A-Z | ^a-z | ^0-9]','',result[10])
	else:
		result_list = [0,0,0,0,0,0]
		return tuple(result_list)
	result_list.append(run)
	result_list.append(hashID)

	return tuple(result_list)


def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

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
	test_readings = db.InstantaneousDemandTest
	test_readings_data = {
		'time':		 	 tuple_msg[0],
		'utcTime':               datetime.datetime.utcnow(),
		'demand':	 	 tuple_msg[1],
		'multiplier': 	         tuple_msg[2],
		'divisor': 		 tuple_msg[3],
		'run': 			 tuple_msg[4],
		'hash': 		 tuple_msg[5]
		
	}
	result = test_readings.insert_one(test_readings_data)
	#Uncomment to test
	print('One post: {0}'.format(result.inserted_id))
	
if __name__ =='__main__':
	mqttc = mqtt.Client("Calit2_Server")
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect

	user = 'dkpljrty'
	password = 'ZJDsxMVKRjoR'
	port = 17934
	broker_address = 'm10.cloudmqtt.com'

	mqttc.username_pw_set(user, password=password)
	mqttc.connect(broker_address, port=port)
	mqttc.subscribe("test_device/readings")
	mqttc.loop_forever()

