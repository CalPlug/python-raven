from MySQLHelper import MySQLHelper
from queue import Queue
from threading import Thread
import paho.mqtt.client as mqtt
import MySQLdb
import MySQLdb.cursors
import datetime
import time


SERVER = 'localhost'
USER = 'root'
PASSWD = 'root'
DB = 'energychannel'

#Callbacks
def on_connect(client, userdata, flags, rc):

	print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):

	print("message received ", str(msg.payload.decode("utf-8")))
	print("message topic=", msg.topic)
	print("message qos=", msg.qos)
	print("message retain flag=", msg.retain)

#Threaded Workers
def keyboardHandling():

	enter = input('Press Enter key to exit...')
	while True:
		if(enter == ""):
			return

def pushToMQTT(q, mqttc):
	
	while True:
		#print("Pushing")
		payload = str(q.get())	
		mqttc.publish("test_device/readings", payload=payload)
		#time.sleep(4)

def getFromMySQL(q,cursor, conn):
	
	prev_datetime = ''	
	while True:	
		conn = MySQLdb.connect(host=SERVER, user=USER, passwd=PASSWD, db=DB, cursorclass = MySQLdb.cursors.SSCursor)
		cursor = conn.cursor()
		cursor.execute("SELECT * from instantaneous_demand WHERE time=(SELECT MAX(time) FROM instantaneous_demand)")	
		row = cursor.fetchone()
		#Uncomment to test		
		if(row[1] == '-1'):
			time.sleep(3)	
			continue		
		if(row[0] == prev_datetime):
			continue 	
		print(str(row))	
		q.put(row)
		prev_datetime = row[0]	      	
		time.sleep(3)	
		cursor.close()

if __name__ =='__main__':

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


	connection = MySQLdb.connect(host=SERVER, user=USER, passwd=PASSWD, db=DB, cursorclass = MySQLdb.cursors.SSCursor)

	cursor = connection.cursor()
	#Queue to act as piping for threads
	q = Queue(maxsize=0)
	#Setting up thread workers
	keyboardHandler = Thread(target=keyboardHandling)

	publishingWorker = Thread(target=pushToMQTT, args=(q,mqttc,))
	publishingWorker.setDaemon(True)

	fetchingWorker = Thread(target=getFromMySQL, args=(q,cursor,connection))
	fetchingWorker.setDaemon(True)
	#Starting
	fetchingWorker.start()
	publishingWorker.start()
	keyboardHandler.start()
	keyboardHandler.join() #Wait for keyboardHandler to return

