"""
    Copyright (C) 2018  George Vasios and Dimitris Kalpaktzidis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import urllib.parse as parser
import urllib.request

import checker
from API_Keys import GEOCODE_API_KEY
from constants import BASE_GEOCODE_URL


# self sustained class
class Geocoder():

    def __init__(self, region):
        self.location = {}
        self.region = region

    # call API to get the geocode of region
    # returns the dict the latitude and longitude
    def get_geocode(self):
        req = urllib.request.Request(BASE_GEOCODE_URL + parser.urlencode({'address': self.region,
                                                                          'key': GEOCODE_API_KEY}))
        response = urllib.request.urlopen(req).read()
        # get json contents
        contents = json.loads(response.decode('utf-8'))

        check = checker.ApiChecker(contents, 'geocode')
        # check status for initial request
        check.check_response_status()

        if not check.get_status() or check.get_zero_res_query():
            return None

        # get geocode
        self.location = contents['results'][0]['geometry']['location']
        return self.location
