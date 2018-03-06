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
import re
import urllib.parse as parser
import urllib.request

import checker
import geocoder
from API_Keys import PLACES_API_KEY
from constants import ERROR_MESSAGE
from etc import fuzzy_comp
from nlp import capture_group_from_regex
from plot import plotter

BASE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

PRICE_LEVELS = {0: 'Free', 1: 'Inexpensive', 2: 'Moderate', 3: 'Expensive', 4: 'Expensive'}


# default radius is 2000 meters
# use maxprice with possible values ranging from 0(affordable) to 4(expensive)
def search_places(query='', maxprice=4, radius='2000'):
    bot_response = []

    query = process_input(query)
    if query == ERROR_MESSAGE:
        return ERROR_MESSAGE, True

    api_type = closest_type(query[0])

    geocode = geocoder.Geocoder(query[1])

    location = geocode.get_geocode()

    if location is None:
        return ERROR_MESSAGE, True

    formatted_location = [str(location['lat']) + ',' + str(location['lng'])]
    parameters = parser.urlencode({'keyword': query, 'location': formatted_location, 'region': 'gr',
                                   'opennow': '', 'radius': radius, 'type': api_type, 'maxprice': maxprice,
                                   'rankby': 'prominence',
                                   'key': PLACES_API_KEY}, doseq=True)

    # performs a nearby on the specified query
    req = urllib.request.Request(BASE_PLACES_URL + parameters)

    response = urllib.request.urlopen(req).read()
    contents = json.loads(response.decode('utf-8'))

    check = checker.ApiChecker(contents, 'places')
    # check status for initial request
    check.check_response_status()

    if not check.get_status() or check.get_zero_res_query():
        return None, True

    results = contents['results']

    latitudes = [location['lat']]
    longitudes = [location['lng']]

    for result in results:
        # get price level
        price_level = PRICE_LEVELS[result['price_level']]
        # check if there is rating
        if 'rating' in result:
            bot_response.append("Open now: {}, Place: {}, Address: {}, Price level: {} and Rating: {}".format(
                str(result['opening_hours']['open_now']), result['name'], str(result['vicinity']),
                price_level, str(result['rating'])))

        else:
            bot_response.append("Open now: {}, Place: {}, Address: {}, Price level: {}".format(
                str(result['opening_hours']['open_now']), result['name'], str(result['vicinity']),
                price_level))

        # needed for plotter
        latitudes.append(result['geometry']['location']['lat'])
        longitudes.append(result['geometry']['location']['lng'])

    plotter(latitudes, longitudes)

    if not bot_response:  # if bot_response is an empty list
        return None, True
    else:
        return bot_response, False


def process_input(message: str):
    things_to_search = ["type", "city"]

    # catches both restaurant and restaurants (in case the Speech Recognition system cannot catch the 's')
    regex = "what are the nearest (?:(restaurants?|cafes?|shopping malls?|gyms?|" \
            "museums?|bakeries?|banks?|bars?)) in (.*?)?(?:\??)$"

    if re.search(regex, message, re.IGNORECASE) is None:
        return ERROR_MESSAGE

    results = capture_group_from_regex(message, regex, things_to_search)

    type = results["type"]
    city = results["city"]

    if type is None or city is None:
        return ERROR_MESSAGE

    return [type, city]


# compares the type from input with the API supported
# types and compares them for better results
def closest_type(place_type):
    place_types = ["restaurant", "cafe", "shopping_mall", "gym",
                   "museum", "bakery", "bank", "bar"]

    for place in place_types:
        if fuzzy_comp(place, place_type):
            return place
