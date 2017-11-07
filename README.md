# python-raven

Coding Development by: Hamed Ghafarshad and Viet Than Ly

Managed by: Dr. Michael Klopfer, Dr. Sergio Gago, Prof. G.P. Li

California Plug Load Research Center (CalPlug), California Institute of Telecommunications and Information Technology (Calit2), University of California, Irvine

CalPlug acknowledges the support of Southern California Edison for the development of this work as part of the "EnergyChannel" project.

Copyright (C) Regents of the University of California, 2017



This is a set of multi-threaded logging scripts written in Python 2.7 and tested in Ubuntu 16.04 that allows a Rainforrest Automation Raven and EMU-2 smart meter HAN interface devices.

The code as written provides 3 functions:

1) Meter to SQL - the meter data will be stored locally in a mySQL database (tested with MySQL 5.5)

2) Meter to SQL then SQL to MQTT - the use of an addon script provides repeating of the local database to and MQTT broker 

3) Meter to MQTT - direct reporting of reported values to an MQTT broker.

Included is a script that reads from a broker and if an updated entry is passed to the broker, these are read, parsed, and inserted in a Mongo DB database.

For the SQL logging capability, a pre-made SQL database with a pair of tables named "instantaneous_demand" and "run_info" is required.  The structure of the tables is as follows:

1) The "instantaneous_demand" table has columns for time, demand, multiplier, divisor, run (designated run name), and hash.  

2) The "run_info" table has columns for "name (run name which matches the data in "instantaneous_demand" table), hash, meter_id, time.


WARNING:  As the SQL logging scripts can read a point every 5-10 seconds from the meter, extended runs of these scripts can lead to large database sizes.  If this script is run on a low power device, performance can degrade with time unless there is another script or operation that is used to purge or archive historic entries.  You are warned!  Occasionally a parsing error will show up for the first read, ignore this.  Reading will be OK after this first issue.  

