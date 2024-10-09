from datetime import datetime, timedelta
import urllib.parse
from urllib3 import PoolManager
from urllib3.util import Retry
import xml.etree.ElementTree as ET

from common.zipcodes import local_zips

BASE_WEATHER_URL = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php'


def get_weather_url(start_hour, end_hour, zip_list):
    tomorrow = datetime.today() + timedelta(days=1)
    start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, start_hour, 0, 0)
    end_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, end_hour, 0, 0)

    params = {
        'whichClient': 'NDFDgenMultiZipCode',
        'zipCodeList': ' '.join(zip_list),
        'product': 'time-series',
        'begin': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'end': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'Unit': 'e',
        'temp': 'temp',
        'Submit': 'Submit'
    }

    query_string = urllib.parse.urlencode(params)

    return f"{BASE_WEATHER_URL}?{query_string}"


def get_weather_data(url):
    retries = Retry(total=5, backoff_factor=0.1)
    http = PoolManager(retries=retries)
    resp = http.request("GET", url)
    return resp.data


def parse_weather_data(xml_text):
    '''
    Parse xml data from weather serive.
    Each temperature element represents a zipcode and has
    value for each hour. This returns the minimum value for each zipcode,
    which should be the minimum temperate over the range of hours requested.
    '''
    root = ET.fromstring(xml_text)

    # This is just being defensive in case we get null values from the API
    # In this case we set the temp to None
    mins = [min((int(t.text) for t in temp_set.iter('value') if t.text is not None), default=None)
            for temp_set in root.iter('temperature')]

    return dict(zip(local_zips, mins))
