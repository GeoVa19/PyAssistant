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

import goslate
import nltk
from PyDictionary import PyDictionary
from word2number.w2n import word_to_num

from constants import LANGUAGE_DICTIONARY, CURRENCIES, ERROR_MESSAGE
from currency_conv import convert
from etc import fuzzy_comp, get_value_from_dictionary

dictionary = PyDictionary()


def extract_entities(text: str, debug=False):
    """
    This function extracts all the Named Entities from text.

    :param text: string
    :param debug: optional (default=False); the function will print additional information if set to True
    :return: a list with all the Named Entities from text
    """
    wikipedia_flag = 0
    result = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                answer = ' '.join(c[0] for c in chunk)
                # TODO add comment
                if fuzzy_comp(answer, "wikipedia") and wikipedia_flag == 0:
                    wikipedia_flag += 1
                    continue

                if debug:
                    print(chunk.label(), ' '.join(c[0] for c in chunk))
                    print(chunk.label())
                    print(answer)
                    print()

                result.append(answer)

    return result


def py_dictionary_utils(message: str, flask=False):
    """
    Given a message in a specific format, print the meaning or synonym or antonym of a word in message.
    Example of a valid format: "{What's the} (meaning || synonym || antonym) {of || for} {the word} ({hello})"
    Valid examples: "What's the the meaning of life", "Find a synonym for the word intelligence", "antonym tall".
    Invalid examples: "hello meaning", "idiot synonym".

    Explanation: the text inside {} denotes an optional text,
                 the text inside () is obligatory,
                 || is the OR operator.
    :param message: string
    :param flask: optional (default=False) True if the application is running as a web app; False otherwise
    :return: the meanings/synonyms/antonyms of a word; if none found, returns an error message
    """
    result = None

    message = message.lower().replace("?", "")

    tokenized_message = message.split()
    word = tokenized_message[-1]

    if message.find("meaning") != -1:
        result = dictionary.meaning(word)
    elif message.find("synonym") != -1:
        result = dictionary.synonym(word)
    elif message.find("antonym") != -1:
        result = dictionary.antonym(word)

    if flask and type(result) is dict:
        for key, values in result.items():
            result = " ".join(key)
            for value in values:
                result = " ".join(value)

    if result is None:
        result = "I don't have that word in my dictionary."

    return result


def capture_group_from_regex(message: str, regex: str, things_to_search: list):
    """
    This function checks if message matches a regular expression.

    :param message: string
    :param regex: string; a regular expression
    :param things_to_search: ...
    :return: a list with the values of the regex groups
    """
    results = {}
    m = re.search(regex, message, re.IGNORECASE)
    if m:
        for i in range(len(things_to_search)):
            try:
                results[things_to_search[i]] = m.group(i + 1)
            except IndexError:
                break
        return results
    return None  # if message does not match the regex


def translate(message: str):
    """
    This function translates a text from a given message. The message has to follow a specific format.
    Example of a valid format: "(Translate) ({hello world}) (in) ({Arabic})"
    Valid examples: "Translate how are you in Swedish", "Translate what's up in Japanese",
        "Translate translate how are you in French in Greek" => "μετάφρασε τι κάνεις στα γαλλικά"
    Invalid examples: "artificial intelligence is awesome in Vietnamese", "Italian I love to sing",
        "Translate what's the weather like Swahili"

    Explanation: the text inside {} denotes an optional text,
                 the text inside () is obligatory.
    :param message: a string that contains the sentence to translate in X language
    :return: the translated text and a boolean which indicates if an error happened
    """
    things_to_search = ["sentence", "language"]

    regex = "translate (.+) in (.*?)$"

    gs = goslate.Goslate()

    if re.search(regex, message, re.IGNORECASE) is None:
        return ERROR_MESSAGE, True

    results = capture_group_from_regex(message, regex, things_to_search)

    sentence_to_translate = results["sentence"]
    language = results["language"]

    # returns an ISO 639-1 language code
    language_code = get_value_from_dictionary(language, LANGUAGE_DICTIONARY, ratio=80)

    if sentence_to_translate is None or language_code is None:
        return ERROR_MESSAGE, True

    try:
        translated_text = gs.translate(sentence_to_translate, language_code)  # call Google Translate API
        return "The translation is {}".format(translated_text), False
    except:
        return "It seems that I am unable to translate the sentence you provided at the moment. " \
               "Please try again in a while.", True


def currency_convert(message: str):
    """
    This function captures the amount of money, the from_currency and the to_currency, and performs the conversion
    from the one currency to the other.
    :param message:
    :return: the results
    """
    things_to_search = ["amount", "quantity", "from_currency", "to_currency"]

    regex = "convert (\d+|\d+\.\d+)\s?(?:(hundred billion|" \
            "hundred million|hundred thousand|billion|million|thousand|hundred)?) (.*?) to (.*?)$"

    if re.search(regex, message, re.IGNORECASE) is None:
        return ERROR_MESSAGE

    results = capture_group_from_regex(message, regex, things_to_search)

    amount = results["amount"]  # get the amount to be converted
    quantity = results["quantity"]  # hundred/thousand/...

    from_currency = results["from_currency"]  # get the from currency name
    to_currency = results["to_currency"]  # get the to currency code name

    from_currency = get_value_from_dictionary(from_currency, CURRENCIES, ratio=60)
    to_currency = get_value_from_dictionary(to_currency, CURRENCIES, ratio=60)

    if from_currency is None or to_currency is None:
        return ERROR_MESSAGE

    total_amount = float(amount) * word_to_num(quantity) if quantity is not None else float(amount)

    conversion_result = convert(from_currency, total_amount, to_currency)

    return conversion_result
