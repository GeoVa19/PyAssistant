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

import aiml
from flask import Flask, render_template, request, jsonify

import how
from constants import BRAIN_FILE, STARTUP_XML_FILE_NAME
from etc import is_wikipedia_search, fuzzy_comp, find, Help
from nearby_places import search_places
from nlp import py_dictionary_utils, translate, currency_convert
from weather import Weather
from wikipedia_api import Wikipedia

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
def ask():
    message = str(request.form['messageText'])

    if message is None:
        return jsonify({'status': 'OK', 'answer': None})

    is_wikipedia_query = is_wikipedia_search(message)
    is_translation_query = fuzzy_comp(message.split()[0], "translate")
    is_nearest_places_query = "nearest" in message.lower()

    if fuzzy_comp(message, "I need some help"):
        bot_response = help.print_help()
    elif find(message, py_dictionary_list):
        bot_response = py_dictionary_utils(message, flask=True)
    elif is_wikipedia_query:
        wikipedia = Wikipedia(message, flask=True)
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

    return jsonify({'status': 'OK', 'answer': bot_response})


if __name__ == "__main__":
    help = Help(flask=True)
    help.read_help_file()
    kernel = aiml.Kernel()
    kernel.verbose(False)  # True for debug only
    if os.path.isfile(BRAIN_FILE):
        kernel.bootstrap(brainFile=BRAIN_FILE)
    else:
        kernel.bootstrap(learnFiles=STARTUP_XML_FILE_NAME, commands="load aiml b")
        kernel.saveBrain(BRAIN_FILE)
    py_dictionary_list = ["meaning", "synonym", "antonym"]

    app.run(host='0.0.0.0', debug=True, port=8080)
