"""
Module to help interact with SQL database.
"""
import MySQLdb
import sys

# Modify this to choose where to store the database
SERVER = 'localhost'
USER = 'xxxxxxxxx'
PASSWD = 'xxxxxxxxx'
DB = 'energychannel'

class MySQLHelperException(Exception):
	pass

class MySQLHelper:
	"""
	Interface construct with database name
	"""
	# Table Names
	TABLE_DEMAND = 'instantaneous_demand'
	TABLE_RUN_INFO = 'run_info'
	TABLE_MISC = 'misc'

	# Common column names
	KEY_ID = 'id'

	# DEMAND TABLE - Columns
	KEY_INSTANT_DEMAND = 'demand'
	KEY_MULTIPLIER = 'multiplier'
	KEY_DIVISOR = 'divisor'
	KEY_RUN = 'run'
	KEY_DATE_TIME = 'date_time'
	KEY_DEMAND_HASH = 'hash'

	# RUN INFO TABLE - Columns
	KEY_HASH = 'hash'
	KEY_METER_ID = 'meter_id'
	KEY_NAME = 'name'
	KEY_TIME = 'time'

	# MISC TABLE - Columns
	KEY_NAME = 'name'
	KEY_VALUE = 'value'

	# Table Create Statements
#	CREATE_TABLE_DEMAND = 'CREATE TABLE IF NOT EXISTS ' + TABLE_DEMAND \
#		+ '(' + KEY_ID + ' INTEGER PRIMARY KEY, ' + KEY_INSTANT_DEMAND \
#		+ ' INTEGER, ' +  KEY_MULTIPLIER + ' INTEGER, ' + KEY_DIVISOR \
#		+ ' INTEGER, ' + KEY_DATE_TIME + ' INTEGER UNIQUE' + ')'

#	CREATE_TABLE_MISC = 'CREATE TABLE IF NOT EXISTS ' + TABLE_MISC \
#	+ '(' + KEY_ID + ' INTEGER PRIMARY KEY, ' + KEY_NAME + ' TEXT UNIQUE, '\
#	+ KEY_VALUE + ' TEXT' + ')'

	# INSERT Statements
	INSERT_TABLE_DEMAND = 'INSERT INTO {}({}) VALUES(%s,%s,%s,%s,%s)'.format(TABLE_DEMAND, ', '.join([KEY_INSTANT_DEMAND, KEY_MULTIPLIER, KEY_DIVISOR, KEY_RUN, KEY_DEMAND_HASH]))
	INSERT_TABLE_RUN_INFO = "INSERT INTO {}({}) VALUES(%s,%s,'')".format(TABLE_RUN_INFO, ', '.join([KEY_HASH, KEY_NAME, KEY_METER_ID]))
#	INSERT_TABLE_MISC = 'INSERT INTO {} VALUES(?,?,?)'.format(TABLE_MISC)
#	UPDATE_TABLE = 'INSERT INTO {}({}) VALUES(?,?,?) ON DUPLICATE KEY UPDATE '.format(TABLE_MISC,
#		', '.join([KEY_NAME, KEY_VALUE])) + KEY_NAME + ' = VALUES(' + KEY_NAME + '), '\
#		+ KEY_VALUE + ' = VALUES(' + KEY_VALUE+ ')'

	def __init__(self):
		"""
		Initialize the connection the database requires name of the database
		"""

	def insertMiscData(self, pk:int, name:str, value:str):
		"""
		Adds or updates misc data.
		"""
		connection = MySQLdb.connect(host=SERVER, user=USER, passwd=PASSWD, db=DB)
		cursor = connection.cursor()
		values = (pk,name,value)
		try:
			cursor.execute(self.INSERT_TABLE_MISC, values)
			connection.commit()
			# print('Successful insert')
		except MySQLdb.IntegrityError:
			pass
			# print('Attempted insert of duplicate')
		except MySQLdb.Error as e:
			pass
			print("An error occurred inserting data:", e.args[0])
		except:
			pass
			# print('Unknown Error: Traceback:', sys.exc_info()[0])
		cursor.close()
		connection.close()
	
	def insertRunInfo(self, data:tuple):
		"""
		Adds a new row to the the table 'run_info'. 
		Format of data is as follows:
		['hash', 'name']

		The types are string and string respectively
		"""
		connection = MySQLdb.connect(host=SERVER, user=USER, passwd=PASSWD, db=DB)
		cursor = connection.cursor()
		try:
			run_info = tuple(data)
			cursor.execute(self.INSERT_TABLE_RUN_INFO, run_info)
			connection.commit()
			# print('Successful insert')
		except MySQLdb.IntegrityError as e:
			pass
			#print('Attempted insert of duplicate')
		except MySQLdb.Error as e:
			pass
			print("An error occurred inserting data:", e.args[0])
		except:
			pass
			print('Unknown Error: Traceback:', sys.exc_info()[0])
		cursor.close()
		connection.close()
			
	def insertDemandData(self, data:tuple):
		"""
		Adds a new row to the table 'instantaneous_demand'. 
		Format of data is as follows:
		['instantaneous_demand', 'multiplier', 'divisor']

		The types are float, float, float, int respectively
		"""
		connection = MySQLdb.connect(host=SERVER, user=USER, passwd=PASSWD, db=DB)
		cursor = connection.cursor()
		try:
			instant_demand = tuple(data)
			cursor.execute(self.INSERT_TABLE_DEMAND, instant_demand)
			connection.commit()
			# print('Successful insert')
		except MySQLdb.IntegrityError:
			pass
			print('Attempted insert of duplicate')
		except MySQLdb.Error as e:
			pass
			print("An error occurred inserting data:", e.args[0])
		except:
			pass
			print('Unknown Error: Traceback:', sys.exc_info()[0])
		cursor.close()
		connection.close()

	def getRecentRows(self, t: int)-> list:
		"""
		Retrieves the rows that were recorded after t
		t is in unix time (i.e. seconds after epoch)
		"""
		self._cursor.execute('SELECT * FROM demand WHERE date_time > (?) ORDER BY date_time DESC', (t,))
		return self._cursor.fetchall()
		
	def getLastNrows(self, n: int)-> list:
		"""
		Returns the last n rows of the database, ordered by date_time.
		Format is as follows:
		('id INTEGER primary key', 'instantaneous_demand REAL', 'multiplier REAL', 'divisor REAL', 'date_time INTEGER') 
		"""
		self._cursor.execute('SELECT * FROM demand ORDER BY date_time DESC LIMIT (?)', (n,))
		return self._cursor.fetchall()

if __name__ == '__main__':
	pass
#	test = MySQLHelper('test.db')
#	test.insertMiscData(1,'temperature', '44')
#	test.insertMiscData(1,'temperature', '55')
#	test.insertMiscData(2, 'location', '1234 Cherry Tree Lane')
#	test.insertDemandData([1,2,3,4])
#	test.close()
#	connection = MySQLdb.connect('test.db')
#	cursor = connection.cursor()
#	for x in cursor.execute('SELECT * FROM misc').fetchall():
#		print(x)
#	cursor.close()
#	connection.close()

