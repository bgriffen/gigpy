from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from datetime import datetime
from datetime import datetime,timedelta
import helper
import logging


def generate_urls_for_next_period(city, num_weeks, window_size):
    """
    Generate URLs for the upcoming n weeks to scrape BandsInTown data.

    :param city: A string representing the city name
    :param num_weeks: An integer representing the number of weeks
    :param window_size: An integer representing the number of days in window
    :return: A list of Strings where each string is a URL for a given week
    """
    base_url = "https://www.bandsintown.com/choose-dates/genre/all-genres"
    city_id = helper.city_to_id[city]

    current_date = datetime.now()
    end_date = current_date + timedelta(weeks=num_weeks)

    urls = []

    while current_date < end_date:
        start_date_block = current_date.date()
        end_date_block = (current_date + timedelta(days=window_size)).date()

        url = f"{base_url}?city_id={city_id}&date={start_date_block.isoformat()}T00:00:00,{end_date_block.isoformat()}T23:59:59&date_filter=This+Week"
        print(url)
        urls.append(url)

        current_date = current_date + timedelta(days=window_size)

    return urls

MATCH_ALL = r'.*'
def like(string):
    """
    Construct a compiled regular expression for the given string

    :param string: A string to construct regex from
    :return: A compiled regular expression instance
    """

    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)


def find_by_text(soup, text, tag, **kwargs):
    """
    Find the tag in soup that matches all provided kwargs, and contains the text

    :param soup: BeautifulSoup instance
    :param text: Text to look for within tag
    :param tag: HTML tag type to search (e.g. div, a)
    :param kwargs: Additional arguments to filter on the tag
    :return: List of matching tags
    """

    matches = []
    for element in soup.find_all(tag, **kwargs):
        if element.find(text=like(text)):
            matches.append(element)
    return matches

def parse_band(band):
    """
    Extract band information from the HTML tag

    :param band: Soup tag containing band information
    :return: A dictionary containing band's name, venue, datetime and number of interested people
    """

    search_item = band.find_all("div")[2].find_all("div")
    info = {}
    info['band_name'] = search_item[1].text
    info['venue'] = search_item[2].text
    info['dtime'] = search_item[3].text
    info['num_interested'] = search_item[5].text
    return info

def get_bands(city, num_weeks, window_size):
    """
    Scrape BandsInTown data for the upcoming n weeks and generate a dataframe

    :param city: A string representing the city name
    :param num_weeks: An integer representing the number of weeks
    :param window_size: An integer representing numer of days in a window
    :return: A Pandas DataFrame containing the scraped data for each band
    """

    urls = generate_urls_for_next_period(city=city,num_weeks=num_weeks,window_size=window_size)
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    dfis = []
    for urli in urls:
        r = requests.get(urli, headers=header)
        soup = BeautifulSoup(r.text,features="lxml")
        bands = find_by_text(soup," PM","a")
        bandinfo = [parse_band(band) for band in bands]
        dfis.append(pd.DataFrame(bandinfo))
    return pd.concat(dfis).drop_duplicates(['band_name'])

