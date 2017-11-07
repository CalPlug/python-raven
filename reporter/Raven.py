import serial
import xml.etree.ElementTree as ET
from time import sleep

from list_ports_linux import comports
#raven stick 
#RAVEN_PID = 0x8a28
#RAVEN_VID = 1027
# Using EMU-2
RAVEN_PID = 3
RAVEN_VID = 1204

# Refer to http://rainforestautomation.com/wp-content/uploads/2014/02/raven_xml_api_r127.pdf
# if you want to look at the Raven documentation.

class NoDeviceFoundError(Exception):
	""" Exception to raise when there is no RAVEn present."""
	pass

class InvalidFormat(Exception):
	""" Exception to raise when XML tag is not completely formed """
	pass

class Raven:
	"""Wrapper for the Serial device that communicates with the 
	RAVEn. Includes several methods that are more user-friendly.
	"""

	def __init__(self):
		self._raven_list = self._findRaven()
		if not self._raven_list:
			self._raven = None
		else:
			self._raven = serial.Serial(self._raven_list[0].device,
						   baudrate=115200, timeout=.5)
	def exists(self):
		return self._raven != None
	
	def refresh(self):
		"""Searches across all USB ports to find a RAVEn device.
		"""
		self._raven_list = self._findRaven()
		if self._raven:
			self.close()
		if len(self._raven_list):
			self._raven = serial.Serial(self._raven_list[0].device,
							baudrate=115200)
		else:
			self._raven = None

	def write(self, cnf:dict=None,**kwargs) -> None:
		"""Constructs a XML fragment from from either a dictionary or keyword
		arguments. Can only be a dictionary or a keywords only, cannot be a 
		mix of both. 
		"""
		self._check()
		self._raven.reset_input_buffer()
		self._raven.reset_output_buffer()
		temp = cnf if cnf else kwargs
		message = ET.tostring(self._commandTemplate(temp))
		self._raven.write(message)

	def read(self) -> str:
		"""Read XML fragment from the Serial device. 
		"""
		return self._readXMLfragment()

	def close(self):
		self._raven.close()
		
	def _findRaven(self):
		"""Searches across all USB ports and returns a list of all RAVEn 
		device.
		"""
		result = [device for device in comports()
			if device.pid == RAVEN_PID and device.vid == RAVEN_VID]
		return result
	
	def _commandTemplate(self, command:dict) -> ET.Element:
		"""Constructs and returns a XML fragment. """
		result = ET.Element('Command')
		for key,value in command.items():
			ET.SubElement(result,key).text = value
		return result

	def _readXMLfragment(self) -> str:
		"""Reads XML fragment, byte by byte. Continues until it encounters the end
		tag.
		"""
		self._check()
		self._raven.reset_output_buffer()
		self._raven.reset_input_buffer()
		first_char = self._raven.read()
		while (first_char == 0 or first_char == b' '):
			first_char = self._raven.read()
		if (first_char != b'<'):
			self._clear()
			raise InvalidFormat('INVALID CHAR: {}'.format(first_char))
		start_tag = first_char
		result = ''
		while (start_tag[-1] != 62):
			char = self._raven.read()
			if len(char) == 0:
				raise Exception('No data')
			start_tag += char
		start_tag = start_tag.decode('ascii').strip('\x00')
	# Debugging
	#	print(start_tag)
		if "/" in start_tag:
			raise InvalidFormat('"/" detected in XML starting tag')
		result = start_tag
		end_tag = start_tag[0] + '/' + start_tag[1:] 
		end_tag_len = len(end_tag)
		while (result[-end_tag_len:] != end_tag):
			char = self._raven.read()
			if len(char) == 0:
				raise Exception('No data')
			result += char.decode('ascii')
		try:
			return ET.fromstring(result)
		except:
			raise InvalidFormat

	def _check(self):
		"""Raises NoDeviceFoundException if no RAVEn is found.
		"""
		if not self._raven:
			raise NoDeviceFoundException
	def _clear(self):
		self._raven.reset_output_buffer()
		self._raven.reset_input_buffer()


if __name__ == '__main__':
	raven_device = Raven()
	if not raven_device._raven:
		print('None found. Please connect the RAVEn')
	else:
		while True:
			input_command = input('Please input a command. Type "quit" to exit.\n')
			if input_command == 'quit':
				break
			input_command = {'Name':input_command}
			
			raven_device.write(input_command)
			# Sleeping the device for a little to allow RAVEN to process
			# the XML fragment.
			sleep(.1)
			try:
				response = raven_device.read()
				print(ET.tostring(response))
			except:
				print("error")
		raven_device.close()
