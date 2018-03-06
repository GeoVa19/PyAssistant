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
import sys
import time
from random import randint, seed

import urllib3
from fuzzywuzzy import fuzz
from playsound import playsound

from constants import PROMPT_FILE_NAME
from speak import speak_and_print


def welcome():
    """
    Prints a welcome message.
    """
    speak_and_print("Hi, I am PyBot, your personal assistant.")


def goodbye(normal_exit=True):
    """
    Prints a goodbye message chosen randomly from a set of three.

    :param normal_exit: optional (default=True); if True, then the program ended due to user's input,
    else the program ended due to failure to connect to the Internet
    """
    seed(None)  # use time as seed
    random_number = randint(0, 2)

    if normal_exit:
        if random_number == 0:
            message = "Goodbye, it was nice talking with you."
        elif random_number == 1:
            message = "See you later."
        else:
            message = "I am looking forward to talking with you again."
    else:
        if random_number == 0:
            message = "I am unable to use the Internet at the moment. Please check your Internet connection."
        elif random_number == 1:
            message = "I am sorry, the Internet and I aren't talking right now."
        else:
            message = "I can't connect at the moment. Try again in a while."

    speak_and_print(message)
    sys.exit(0 if normal_exit else 1)


def prompt(fname=PROMPT_FILE_NAME):
    """
    Plays a sound that prompts user for input. 
	
	You can add an .mp3 file. 
	In that case, you can remove the speak_and_print() call and call playsound() instead.

    :param fname: optional
    """
    # playsound(fname)
    speak_and_print("Please insert your query.")


def remove_parentheses(text):
    # text = remove_multiple_whitespaces(text)
    # text = remove_punctuation(text)
    text = re.sub(r"\([^)]*\)", "", text)

    return text


"""
def remove_multiple_whitespaces(text):
    return ' '.join(text.split())


# https://stackoverflow.com/questions/11066400/remove-punctuation-from-unicode-formatted-strings/21635971
def remove_punctuation(text):
    tbl = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))
    return text.translate(tbl)
"""


def internet_connection(url="http://www.google.com"):
    """
    Detects if there is an Internet connection.

    :param url:
    :return: True if there is connection to the Internet, otherwise False
    """
    http = urllib3.PoolManager()

    try:
        response = http.request('HEAD', url)
        return True
    except urllib3.exceptions.MaxRetryError:
        return False


def check_internet_connection():
    """
    Checks if there is an Internet connection. If not, the program exits with a normal_exit set to False.
    """
    if not internet_connection():
        goodbye(normal_exit=False)


def find(message: str, tokens: list):
    """
    Checks if the message contains a token in tokens.

    :param message: string
    :param tokens: a list of tokens
    :return: True if the message contains one of the tokens, otherwise False
    """
    for token in tokens:
        if message.find(token) != -1:
            return True


def is_wikipedia_search(query: str):
    """
    Checks whether the user's query needs a call to Wikipedia.

    :param query: string
    :return: True if the user wants to do a Wikipedia search, otherwise False
    """
    tokens = query.split()
    if fuzzy_comp(tokens[0], "wikipedia"):
        return True
    return False


def fuzzy_comp(word_one: str, word_two: str, ratio=80):
    """
    This function does a fuzzy comparison between two words.

    :param word_one: string
    :param word_two: string
    :param ratio: optional (default=80);
    :return: True if word_one is fuzzily equal to word_two, otherwise False
    """
    return fuzz.ratio(word_one, word_two) > ratio


def get_value_from_dictionary(requested_key: str, dictionary: dict, ratio: int):
    """
    This function searches if requested_key belongs to a dictionary.

    :param requested_key:
    :param dictionary:
    :param ratio:
    :return: the respective key
    """
    for key in dictionary:
        if fuzzy_comp(key, requested_key, ratio):
            return dictionary[key]
    return None


class Help:
    def __init__(self, flask=False):
        self.help_list = []
        self.flask = flask

    def read_help_file(self):
        """
        This method loads all tips from file to memory.
        """
        with open("help.txt", "r") as f:
            self.help_list = [line.rstrip('\n') for line in f]

    def print_help(self):
        """
        This method prints all tips to screen.
        The program sleeps for 15 sec, which allows the user to read the tips carefully.
        """
        if not self.flask:
            speak_and_print("Here are some things I can help you do.")
            for tip in self.help_list:
                print(tip)
            time.sleep(15)
        else:
            tips = "<br />".join(self.help_list)
            return tips
