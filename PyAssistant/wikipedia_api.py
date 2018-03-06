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
from random import randint

import wikipedia as wiki

from etc import fuzzy_comp
from listen import listen
from nlp import extract_entities
from speak import speak_and_print


class Wikipedia:

    def __init__(self, query, flask=False):
        self.query = query
        self.entities = extract_entities(query)
        self.article = None
        self.possible_articles = None
        self.flask = flask

    def get_summary_for_entities(self):
        """
        Given a list of entities, call get_summary function for each entity.

        :param entities: a list of Named Entities
        :return:
        """
        summaries = []
        for entity in self.entities:
            summaries.append(self.__get_summary(entity))
        return summaries

    def __get_summary(self, entity):
        """
        This method performs a Wikipedia search on query, and shows a summary of the article to the user.

        :param query; a query to search on Wikipedia
        :return: the article of the object
        """
        try:
            find_query = wiki.search(entity, 1)
            self.article = wiki.summary(find_query, 1)
            self.__format_wikipedia_article()

            return self.article
        except wiki.PageError:
            speak_and_print("Sorry, there were no matches to your query.")
        except wiki.exceptions.DisambiguationError:
            return self.__disambiguate_articles()
        except wiki.HTTPTimeoutError:
            speak_and_print("Sorry, server time out. Please try again in a while.")
        except:
            speak_and_print("Sorry, something went wrong.")

    def __disambiguate_articles(self):
        """
        This method runs in case query results to a list of Wikipedia articles (and not just one),
        therefore the user has to choose which article (s)he wants.

        :return: the article of the object
        """
        self.possible_articles = wiki.search(self.query)

        if self.query in self.possible_articles:  # search if query is in possible_articles list
            self.possible_articles.pop(self.possible_articles.index(self.query))  # remove query from the list

        if not self.flask:
            answer_index = self.__choose_article()  # get the index of the name of the article
        else:
            answer_index = randint(0, len(self.possible_articles) - 1)

        self.article = wiki.summary(self.possible_articles[answer_index])  # get the summary of the chosen article

        self.__format_wikipedia_article()

        return self.article

    def __choose_article(self):
        possible_answers = []
        index = 0

        speak_and_print("Which one of the following do you mean?")

        # print the index and the name of each article in possible_articles list
        for article in self.possible_articles:
            print("{key} -> {value}".format(key=str(index + 1), value=article))
            possible_answers.insert(index, article)
            index += 1

        speak_and_print("Which one?")

        user_response = listen()

        article_index = -1

        while article_index == -1:
            for index, possible_answer in enumerate(possible_answers):
                if fuzzy_comp(possible_answer, user_response):
                    article_index = index
                    return article_index
            user_response = listen()
            if user_response is None:
                continue

    def __format_wikipedia_article(self):
        self.article = "According to Wikipedia.org, {}".format(self.article)
