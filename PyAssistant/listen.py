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
import speech_recognition as sr

from etc import prompt, check_internet_connection
from speak import speak_and_print


def listen(keyboard=False):
    """
    This function prints and returns user's input (None in case of an error). Input is via microphone or keyboard.

    :param keyboard: optional (default=False); if True, input is via keyboard, else input is via microphone
    :return: user's query or None if an error happened
    """
    if not keyboard:
        check_internet_connection()  # connection to the Internet is necessary
        prompt()  # play sound prompt

        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                audio = r.listen(source)

                query = r.recognize_google(audio, language="en-US")  # call Google Speech Recognition API
                print(query)
            return query
        except sr.UnknownValueError:
            error_message = "Sorry, I didn't catch that."
            speak_and_print(error_message)
            return None
    else:
        speak_and_print("Please insert your query.")
        prompt()
        user_input = input()
        return None if len(user_input) == 0 else user_input
