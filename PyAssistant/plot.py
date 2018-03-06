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
import webbrowser as browser
from pathlib import Path
from pathlib import WindowsPath as path

import gmplot as plot

from API_Keys import MAPS_JAVASCRIPT_API_KEY


# plots current location and found places
# from user defined query, to Google Maps
def plotter(latitudes, longitudes):
    gmap = plot.GoogleMapPlotter(latitudes[0], longitudes[0], zoom=15, apikey=MAPS_JAVASCRIPT_API_KEY)
    # gmap.plot(latitudes, longitudes, '#C71585', edge_width=1)
    # markers only over places and not current location
    gmap.scatter(latitudes[1:], longitudes[1:], '#C71585', size=50, marker=False)

    # create html file
    gmap.draw("places.html")
    open_in_browser()


# checks if places.html file exists
def open_in_browser():
    maps_file_path = Path(str(path.cwd()) + '/places.html')
    if maps_file_path.exists():
        try:
            browser.open_new_tab(str(maps_file_path))
        #            print("Opening browser...")
        except browser.Error:
            print('Something went wrong...')
    else:
        print('File, places.html has not been created!')
