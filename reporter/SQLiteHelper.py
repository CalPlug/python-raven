"""
Module to help interact with SQL database.
"""
import sqlite3
import sys

class SQLHelperException(Exception):
	pass

class SQLiteHelper:
	"""
	Interface construct with database name
	"""
	# Table Names
	TABLE_DEMAND = 'demand'
	TABLE_MISC = 'misc'

	# Common column names
	KEY_ID = 'id'

	# DEMAND TABLE - Columns
	KEY_INSTANT_DEMAND = 'instantaneous_demand'
	KEY_MULTIPLIER = 'multiplier'
	KEY_DIVISOR = 'divisor'
	KEY_DATE_TIME = 'date_time'

	# MISC TABLE - Columns
	KEY_NAME = 'name'
	KEY_VALUE = 'value'

	# Table Create Statements
	CREATE_TABLE_DEMAND = 'CREATE TABLE IF NOT EXISTS ' + TABLE_DEMAND \
		+ '(' + KEY_ID + ' INTEGER PRIMARY KEY, ' + KEY_INSTANT_DEMAND \
		+ ' INTEGER, ' +  KEY_MULTIPLIER + ' INTEGER, ' + KEY_DIVISOR \
		+ ' INTEGER, ' + KEY_DATE_TIME + ' INTEGER UNIQUE' + ')'

	CREATE_TABLE_MISC = 'CREATE TABLE IF NOT EXISTS ' + TABLE_MISC \
	+ '(' + KEY_ID + ' INTEGER PRIMARY KEY, ' + KEY_NAME + ' TEXT UNIQUE, '\
	+ KEY_VALUE + ' TEXT' + ')'

	# INSERT Statements
	INSERT_TABLE_DEMAND = 'INSERT INTO {}({}) VALUES(?,?,?,?)'.format(TABLE_DEMAND,
			', '.join([KEY_INSTANT_DEMAND, KEY_MULTIPLIER, KEY_DIVISOR, KEY_DATE_TIME]))
	INSERT_TABLE_MISC = 'INSERT INTO {} VALUES(?,?,?)'.format(TABLE_MISC)
	UPDATE_TABLE = 'INSERT INTO {}({}) VALUES(?,?,?) ON DUPLICATE KEY UPDATE '.format(TABLE_MISC,
		', '.join([KEY_NAME, KEY_VALUE])) + KEY_NAME + ' = VALUES(' + KEY_NAME + '), '\
		+ KEY_VALUE + ' = VALUES(' + KEY_VALUE+ ')'

	def __init__(self, db_name:str):
		"""
		Initialize the connection the database requires name of the database
		"""
		self._db_name	= db_name
		self._connection = sqlite3.connect(db_name)
		self._cursor	 = self._connection.cursor()
		self._createTables()
		
	def _createTables(self):
		self._cursor.execute(self.CREATE_TABLE_DEMAND)
		self._cursor.execute(self.CREATE_TABLE_MISC)

	def insertMiscData(self, pk:int, name:str, value:str):
		"""
		Adds or updates misc data.
		"""
		values = (pk,name,value)
		try:
			self._cursor.execute(self.INSERT_TABLE_MISC, values)
			self._connection.commit()
			# print('Successful insert')
		except sqlite3.IntegrityError:
			pass
			# print('Attempted insert of duplicate')
		except sqlite3.Error as e:
			pass
			print("An error occurred inserting data:", e.args[0])
		except:
			pass
			# print('Unknown Error: Traceback:', sys.exc_info()[0])
			
	def insertDemandData(self, data:list):
		"""
		Adds a new row to the database. 
		Format of data is as follows:
		['instantaneous_demand', 'multiplier', 'divisor', 'date_time']

		The types are float, float, float, int respectively
		"""
		instant_demand = tuple(data) if isinstance(data,list) else data
		try:
			self._cursor.execute(self.INSERT_TABLE_DEMAND, instant_demand)
			self._connection.commit()
			# print('Successful insert')
		except sqlite3.IntegrityError:
			pass
			print('Attempted insert of duplicate')
		except sqlite3.Error as e:
			pass
			print("An error occurred inserting data:", e.args[0])
		except:
			pass
			print('Unknown Error: Traceback:', sys.exc_info()[0])

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
			
	def close(self):
		"""Closes cursor and connection.
		"""
		self._cursor.close()
		self._connection.close()

	def clear(self):
		self._cursor.execute()

if __name__ == '__main__':
	test = SQLiteHelper('test.db')
	test.insertMiscData(1,'temperature', '44')
	test.insertMiscData(1,'temperature', '55')
	test.insertMiscData(2, 'location', '1234 Cherry Tree Lane')
	test.insertDemandData([1,2,3,4])
	test.close()
	connection = sqlite3.connect('test.db')
	cursor = connection.cursor()
	for x in cursor.execute('SELECT * FROM misc').fetchall():
		print(x)
	cursor.close()
	connection.close()

