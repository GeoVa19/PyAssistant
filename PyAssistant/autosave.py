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
from constants import BRAIN_FILE


class Autosave:

    def __init__(self, kernel):
        self.counter = 1
        self.kernel = kernel

    def autosave(self):
        if self.counter % 10 == 0:
            self.kernel.saveBrain(BRAIN_FILE)
            self.counter = 1

    def increment_counter(self):
        self.counter += 1
