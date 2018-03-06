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
import urllib.parse as parser
import webbrowser as browser

from constants import ERROR_MESSAGE
from nlp import capture_group_from_regex


def open_browser(query):
    search_url = 'https://www.google.com/search?' + parser.urlencode({'q': query})
    try:
        browser.open_new_tab(search_url)
    except browser.Error:
        print('Something went wrong...')

    return


def get_query(message: str):
    things_to_search = ["query"]

    regex = "search (.*?)$"

    if re.search(regex, message, re.IGNORECASE) is None:
        return ERROR_MESSAGE

    results = capture_group_from_regex(message, regex, things_to_search)

    query = results["query"]

    if query is None:
        return ERROR_MESSAGE

    return query
