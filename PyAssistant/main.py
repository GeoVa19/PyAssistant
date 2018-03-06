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
import os
import time as t

import aiml

import how
from autosave import *
from constants import STARTUP_XML_FILE_NAME, BRAIN_FILE
from etc import check_internet_connection, welcome, fuzzy_comp, goodbye, find, is_wikipedia_search, \
    Help, remove_parentheses
from listen import listen
from nearby_places import search_places
from nlp import py_dictionary_utils, translate, currency_convert
from speak import speak_and_print, speak
from weather import Weather
from wikipedia_api import Wikipedia

check_internet_connection()

kernel = aiml.Kernel()
kernel.verbose(False)  # True for debug only

help = Help()
help.read_help_file()

if os.path.isfile(BRAIN_FILE):
    kernel.bootstrap(brainFile=BRAIN_FILE)
else:
    kernel.bootstrap(learnFiles=STARTUP_XML_FILE_NAME, commands="load aiml b")
    kernel.saveBrain(BRAIN_FILE)
    welcome()
    help.print_help()

autosave = Autosave(kernel)  # initialize autosave object

py_dictionary_list = ["meaning", "synonym", "antonym"]

while True:
    message = listen()  # get user's query
    bot_response = None

    if message is not None:
        is_wikipedia_query = is_wikipedia_search(message)
        is_translation_query = fuzzy_comp(message.split()[0], "translate")
        is_nearest_places_query = "nearest" in message.lower()

        if fuzzy_comp(message, "goodbye"):
            goodbye()
        elif fuzzy_comp(message, "I need some help"):
            help.print_help()
        elif find(message, py_dictionary_list):
            bot_response = py_dictionary_utils(message)
        elif is_wikipedia_query:
            wikipedia = Wikipedia(message)
            bot_response = wikipedia.get_summary_for_entities()
        elif is_translation_query:
            bot_response, error_happened = translate(message)
        elif "convert" in message.lower():
            bot_response = currency_convert(message)
        elif "weather" in message.lower():
            weather = Weather(message)
            weather.parse_weather_query()
            weather.calculate_coords()
            bot_response = weather.get_weather_data()
        elif "search" in message.lower():
            search_query = how.get_query(message)
            bot_response = how.open_browser(search_query)
        elif is_nearest_places_query:
            bot_response, error_happened = search_places(message)
        else:
            bot_response = kernel.respond(message)
            autosave.increment_counter()
            autosave.autosave()

        if bot_response is None or len(bot_response) == 0:
            continue

        if is_wikipedia_query:
            for summary in bot_response:
                print(summary)
                speak(remove_parentheses(summary))
        elif is_nearest_places_query:
            if error_happened is False:
                speak_and_print("Here's what I found for you.")
                for place_info in bot_response:
                    print(place_info)
            else:
                speak_and_print(bot_response)
        elif is_translation_query:
            if error_happened is False:
                # pyttsx3 library can't speak in other languages other than English, so we just print the result
                # we tried Google's Text-to-Speech engine (with multilingual support), but it needs to store an mp3 file
                # we tried to delete the file once done, but we had problems at deleting the file, so we abandoned it...
                print(bot_response)
            else:
                speak_and_print(bot_response)
        else:
            speak_and_print(bot_response)

    t.sleep(0.5)
