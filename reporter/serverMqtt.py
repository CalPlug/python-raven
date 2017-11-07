import paho.mqtt.client as mqtt
from pymongo import MongoClient

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
	demand_data = str(msg.payload.decode("utf-8"))
	print("message received ", demand_data)
	print("message topic=", msg.topic)
	#print("message qos=", msg.qos)
	#print("message retain flag=", msg.retain)

	'''client = MongoClient('localhost', 27017)
	db = client['pymongo_test']
	test_readings = db.test_readings
	test_readings_data = {
		'time':		 demand_data[0],
		'demand':	 demand_data[1],
		'multiplier': 	 demand_data[2],
		'divisor': 	 demand_data[3],
		'run': 		 demand_data[4],
		'hash': 	 demand_data[5]
		
	}
	result = test_readings.insert_one(test_readings_data)
	print('One post: {0}'.format(result.inserted_id))'''
if __name__ =='__main__':
	mqttc = mqtt.Client("Python")
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect

	user='xxxxxxxxxxxxx'
	password = 'xxxxxxxxxxxxxx'
	port = 16054
	broker_address = 'm10.cloudmqtt.com'

	mqttc.username_pw_set(user, password=password)
	mqttc.connect(broker_address, port=port)
	print("Subscribing to topic", "111/readings")
	mqttc.subscribe("111/readings")
	mqttc.loop_forever()

