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
from functools import lru_cache

BASE_URL = 'https://api.fixer.io/latest?'


@lru_cache(maxsize=1024)  # not sure if it really caches result
def convert(from_currency, amount, to_currency):
    """
    This function converts an amount of money from one currency to an other.

    :param from_currency:
    :param amount:
    :param to_currency:
    :return: the result; if an error happened, an error message
    """

    req = urllib.request.Request(BASE_URL + parser.urlencode({'base': from_currency,
                                                              'symbols': to_currency}))

    try:
        response = urllib.request.urlopen(req).read()
        contents = json.loads(response.decode('utf-8'))
        converted_amount = contents['rates'][to_currency] * amount

        return "{} in {} are {:.2f} in {}".format(amount, from_currency, converted_amount, to_currency)
    except urllib.error.HTTPError:
        return "We don't support one or any of the currencies you provided."
