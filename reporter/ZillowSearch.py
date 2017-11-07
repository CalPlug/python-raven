import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import namedtuple

ZILLOW_API_KEY = 'X1-ZWz1fcbkspfyff_9r65p'
ZILLOW_GET_SEARCH = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
ZILLOW_PROPERTY_DETAILS = 'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?'

House = namedtuple('House', 'bedrooms bathrooms sq_feet')

class ZillowSearch:

    def getHouse(self, address:str, citystatezip:str) -> House:
        self._getHomeZPID(address, citystatezip)
        house = self.data.find('response').find('results').find('result')
        bedrooms = float(house.find('bedrooms').text)
        bathrooms = float(house.find('bathrooms').text)
        sq_feet = float(house.find('lotSizeSqFt').text)
        return House(bedrooms, bathrooms, sq_feet)


    def _getHomeZPID(self, address:str, citystatezip:str) -> None:
        params = urllib.parse.urlencode(
                {'zws-id' : ZILLOW_API_KEY,
                    'address' : address,
                    'citystatezip' : citystatezip} )
        url = ZILLOW_GET_SEARCH + params
        with urllib.request.urlopen(url) as f:
            self.data = ET.fromstring(f.read().decode('utf-8'))

    def _addressToString(self, address:ET.Element) -> str:
        """Converts XML address to str format.
        """
        street = address.find('street').text
        city = address.find('city').text
        state = address.find('state').text
        zipcode = address.find('zipcode').text
        return '{}, {}, {}, {}'.format(street,city,state,zipcode)

if __name__ == '__main__':
        search = ZillowSearch()
        data = search.getHouse('9122 Brabham Dr.', 'Huntington Beach, CA, 92646')
        
