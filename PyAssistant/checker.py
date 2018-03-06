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
from speak import speak_and_print


class ApiChecker:

    def __init__(self, response, function):
        self.__response = response
        # which function called checker
        self.__function = function
        # properties in order to  act in different errors
        self.__zero_res_loc = False
        self.__zero_res_query = False
        self.__status = False

    def check_response_status(self):
        # if secondary or each next request of each api call
        # is fine, then these variables should be reset to their
        # default values otherwise, infinite loop
        self.__zero_res_loc = False
        self.__zero_res_query = False
        if self.__response['status'] == 'ZERO_RESULTS' and self.__function == 'geocode':
            speak_and_print("Sorry, the entered address is non existent!")
            self.__zero_res_loc = True
        elif self.__response['status'] == 'UNKNOWN_ERROR' and self.__function == 'geocode':
            speak_and_print("There was a server error!")
        elif self.__response['status'] == 'ZERO_RESULTS' and self.__function == 'places':
            self.__zero_res_query = True
            speak_and_print("Sorry, we couldn't find what you are looking for!")
        elif self.__response['status'] == 'OVER_QUERY_LIMIT':
            speak_and_print("The query limit has been exceeded!")
        elif self.__response['status'] == 'REQUEST_DENIED':
            speak_and_print("Your API key is not valid!")
        elif self.__response['status'] == 'INVALID_REQUEST':
            speak_and_print("Your request is invalid!")
        # if status == OK then True
        else:
            self.__status = True

    def get_status(self):
        return self.__status

    def get_zero_res_loc(self):
        return self.__zero_res_loc

    def get_zero_res_query(self):
        return self.__zero_res_query

    def set_response(self, contents):
        self.__response = contents
