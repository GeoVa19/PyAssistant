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
import pyttsx3


def speak(bot_response):
    """
    This function makes the bot speak.

    :param bot_response: message that the bot says
    """
    engine = pyttsx3.init()
    engine.say(bot_response)
    engine.setProperty("rate", 80)
    engine.setProperty("volume", 1)
    engine.runAndWait()


def speak_and_print(bot_response):
    """
    This function makes the bot say and print a message.

    :param bot_response: message that the bot says
    """
    if type(bot_response) in [list, tuple]:  # useful for py_dictionary_utils() from nlp.py
        for item in bot_response:
            print(item)
    elif type(bot_response) is dict:  # same as above
        for key, values in bot_response.items():
            print(key)
            for value in values:
                print(value)
            print()
    else:
        print(bot_response)
    speak(bot_response)
