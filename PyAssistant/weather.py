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
import re

import pyowm

from API_Keys import OPENWEATHERMAP_KEY
from constants import ERROR_MESSAGE
from geocoder import Geocoder
from nlp import extract_entities, capture_group_from_regex


class Weather:
    def __init__(self, query):
        self.owm = pyowm.OWM(OPENWEATHERMAP_KEY)
        self.query = query
        self.city_name = None
        self.is_tomorrow = None
        self.lat = None
        self.lon = None
        self.weather = None
        self.error_happened = None

    def parse_weather_query(self):
        things_to_search = ["city_name", "tomorrow"]

        # catches city/country names, tomorrow (if exists), ignores "?"
        regex = "(?:what's|what is) the weather like in (.*?)(?:(tomorrow))?(?:\??)$"

        if re.search(regex, self.query, re.IGNORECASE) is None:
            self.error_happened = True
            return

        results = capture_group_from_regex(self.query, regex, things_to_search)

        city_name = results["city_name"]

        temp_result = extract_entities(city_name)
        extracted_city_name_list = None if len(temp_result) == 0 else temp_result  # returns list!

        # useful when the NER system does not recognize any entity!
        if extracted_city_name_list is None:
            self.error_happened = True
            return

        extracted_city_name = ' '.join(extracted_city_name_list)

        if extracted_city_name is None:
            self.error_happened = True
            return

        self.is_tomorrow = False if results["tomorrow"] is None else True

        self.city_name = extracted_city_name

    def calculate_coords(self):
        if self.city_name is None:
            return

        geocoder = Geocoder(self.city_name)
        geocode = geocoder.get_geocode()

        if geocode is None:
            return

        self.lat = geocode["lat"]
        self.lon = geocode["lng"]

    def get_weather_data(self):
        if self.lat is None:
            self.error_happened = True
            return self.__show_weather()

        try:
            if not self.is_tomorrow:
                observation = self.owm.weather_at_coords(self.lat, self.lon)
                self.weather = observation.get_weather()
            else:
                tomorrow = pyowm.timeutils.tomorrow()
                forecast = self.owm.daily_forecast_at_coords(self.lat, self.lon)
                self.weather = forecast.get_weather_at(tomorrow)

            return self.__show_weather()
        except pyowm.exceptions.not_found_error:
            self.__show_weather(error_message="I was unable to find {}.".format(self.city_name), exception_error=True)
        except pyowm.exceptions.parse_response_error:
            self.__show_weather(error_message="There was a problem with the OpenWeatherMap.", exception_error=True)
        except pyowm.exceptions.unauthorized_error:
            self.__show_weather(error_message="I was unable to perform that operation.",
                                exception_error=True)  # needs an API key
        except pyowm.exceptions.api_call_error:
            self.__show_weather(error_message="A network error occurred. Please check your Internet connection.",
                                exception_error=True)

    def __show_weather(self, error_message=ERROR_MESSAGE, exception_error=False):
        if self.weather is None or self.error_happened is True or exception_error is True:
            return error_message

        temperature_json = self.weather.get_temperature(unit="celsius")

        wind_json = self.weather.get_wind(unit="miles_hour")
        wind = "{0:.2f}".format(wind_json["speed"] * 1.609344)  # convert wind speed to km/hour

        if not self.is_tomorrow:
            temperature = temperature_json["temp"]
            max_temperature = temperature_json["temp_max"]
            min_temperature = temperature_json["temp_min"]
            humidity = self.weather.get_humidity()
            forecast_description = "According to OpenWeatherMap, the temperature in {} is currently {} Celsius with " \
                                   "wind at {} kilometers per hour. The maximum temperature will be {} Celsius and the minimum {}. " \
                                   "The humidity is {}%.".format(self.city_name, temperature, wind, max_temperature,
                                                                 min_temperature, humidity)
        else:
            max_temperature = temperature_json["max"]
            min_temperature = temperature_json["min"]
            forecast_description = "According to OpenWeatherMap, there will be a minimum temperature of {} Celsius" \
                                   " and a maximum temperature of {} in {} tomorrow. The wind will be at {} kilometers per hour." \
                .format(min_temperature, max_temperature, self.city_name, wind)

        return forecast_description
