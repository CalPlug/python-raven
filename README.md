# python-raven

Logging and Reporting Utilities for Rainforest Automation's Raven and EMU-2 Smart Meter Energy Monitors

Initial Coding Development by: Hamed Ghafarshad and Viet Than Ly  
Development Extended by: Yutien Ren

Managed by: Dr. Michael Klopfer, Dr. Sergio Gago, Prof. G.P. Li

California Plug Load Research Center (CalPlug), California Institute of Telecommunications and Information Technology (Calit2), University of California, Irvine

CalPlug acknowledges the support of Southern California Edison for the development of this work as part of the "EnergyChannel" project.

Copyright (c) Regents of the University of California, 2018

***************************************************************************************************
***************************************************************************************************


This is a set of multi-threaded logging scripts written in Python 3 and tested in Ubuntu 16.04 that allows a Rainforest Automation Raven and EMU-2 smart meter HAN interface devices using their XML API (https://rainforestautomation.com/wp-content/uploads/2014/02/raven_xml_api_r127.pdf).

The reporter code as written provides 3 functions (available in the reporter directory):

1) Meter to SQL - the meter data will be stored locally in a mySQL database (tested with MySQL 5.5)

2) Meter to SQL then SQL to MQTT - the use of an addon script provides repeating of the local database to and MQTT broker 

3) Meter to MQTT - direct reporting of reported values to an MQTT broker.  This effort is similar to https://github.com/stormboy/node-raven but in Python versus node.

Included is a script that reads from a broker and if an updated entry is passed to the broker, these are read, parsed, and inserted in a Mongo DB database (in the recorder directory).

For the SQL logging capability, a pre-made SQL database with a pair of tables named "instantaneous_demand" and "run_info" is required.  The structure of the tables is as follows:

1) The "instantaneous_demand" table has columns for time, demand, multiplier, divisor, run (designated run name), and hash.  

2) The "run_info" table has columns for "name (run name which matches the data in "instantaneous_demand" table), hash, meter_id, time.


WARNING:  As the SQL logging scripts can read a point every 5-10 seconds from the meter, extended runs of these scripts can lead to large database sizes.  If this script is run on a low power device, performance can degrade with time unless there is another script or operation that is used to purge or archive historic entries.  You are warned!  Occasionally a parsing error will show up for the first read, ignore this.  Reading will be OK after this first issue.  

# Accessing Uploaded Records in MongoDB

1) Log into the Calit2 MQTT server(cpmqtt1) using the following credentials:
2) Open the mongo shell
3) Enter command "use pulses"
4) Enter "db.InstantaneousDemandTest.find()" to see all records posted from the Meter to SQL to MQTT add-on. Enter "db.InstantaneousDemandTest1.find()" to see all records posted from the direct Meter to MQTT script.
5) Refer to MongoDB documentation for a list of commands to access specific records

# Meter to SQL script (run.py)

1) Make sure the Raven stick or Rainforest Automation unit is on and attached to a USB port
2) Open the reporter directory inside of python-raven
3) Run the the "run.py" script with the following command : sudo python3 run.py
4) A query prompt will ask you to type in the appropriate name of the run
5) The script will begin sending data to SQL after a 3 2 1 countdown.
6) In the case that the Raven / Rainforest Automation unit is not found, the terminal will display "searching..." repeatedly
7) If it is found successfully, then the rows of data read from the unit and added to the SQL database will display on the screen sequentally.

# Meter to SQL to MQTT Add-on (run.py serverMqtt.py loggerMqtt.py)

1) To start the server to collect data from the MQTT broker to MongoDB, log on to the Calit2 MQTT server(cpmqtt1). 
2) Open the smartmeter directory
3) Run the server script with the following command:
	sudo python3 serverMqtt.py
4) On a successful connection to the MQTT broker, the terminal will display "Connected with result 0"
5) In a seperate terminal execute the run.py script explained under Meter to SQL script instructions
6) Open another terminal
7) Open python-raven/reporter directory
8) Run the loggerMqtt.py script with the following command : sudo python3 loggerMqtt.py
9) On a successful connection to the MQTT broker, the terminal will display "Connected with result 0"
10) Data that are successfully pushed to MQTT will display on the terminal running loggerMqtt.py
11) Data that is pushed to MongoDB will display on the terminal running serverMqtt.py

# Meter to MQTT (direct_mqtt_run.py serverMqttR.py)

Note: This script posts instantaneous demand, current summation delivered and current summation recieved along with a meter Mac ID to a MongoDB table named "InstantaneousDemandTest1". 

1) To start the server to collect data from the MQTT broker to MongoDB, log on to the Calit2 MQTT server(cpmqtt1). 
2) Open the smartmeter directory
3) Run the server script with the following command:
	sudo python3 serverMqttR.py
4) On a successful connection to the MQTT broker, the terminal will display "Connected with result 0"
5) Open a seperate terminal
6) Open the python-raven/recorder directory 
7) Run the direct_mqtt_run.py script with the following command:
	sudo python3 direct_mqtt_run.py
8) On a successful connection to the MQTT broker, the terminal will display "Connected with result 0"
9) Rows of data that are sent from the broker should begin displaying on the terminal.


# Data Visualizer for Internal Usage (main.py data_retriever.py auto_box.py simple_visualizer_v2.py visualizer_internal_v2.py)

Note: This Visualizer is only for interval usage. It may be polished later if necessary and be converted into an .exe or .app file for different OS.

1) Open main.py
2) Fill in the credentials for db and retrieved keys
3) Run main.py
4) Graph will be the first user in the db with auto-generated lower and upper bound for time interval
6) Auto-Complete and Cascade-View for user search box
7) Switch user by clicking Change User
8) After changing time interval, click draw to get graph of the user in the time interval
9) Reset to get defualt graph for the current user in the defualt time interval which bounded by min and max date of record

