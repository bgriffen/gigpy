from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from datetime import datetime
from datetime import datetime,timedelta

cityid = {'Brisbane':2174003,
          'Melbourne':2158177,
          'Sydney':2147714,
          'Adelaide':2078025}

def generate_urls_for_next_nweeks(city,num_weeks):
    """
    To get around BandsInTown display, break into n_week blocks and concat.
    """
    current_date = datetime.now()
    nthblock = 0
    lists  = []
    while nthblock < num_weeks:
        current_block = current_date.date().isoformat()
        Updated_date = current_date+ timedelta(weeks=1)
        laterdate = Updated_date.date().isoformat()
        #return Updated_date.date().isoformat()
        listi = ["https://www.bandsintown.com/",
                "?city_id=","%s"%cityid[city],
                "&date=",current_block,
                "T14%3A00%3A00%2C",laterdate,
                "T23%3A59%3A59&date_filter=This+Week"]
        lists.append("".join(listi))
        current_date = Updated_date
        nthblock +=1

    return lists

MATCH_ALL = r'.*'
def like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)


def find_by_text(soup, text, tag, **kwargs):
    """
    Find the tag in soup that matches all provided kwargs, and contains the
    text.

    If no match is found, return None.
    If more than one match is found, raise ValueError.
    """
    elements = soup.find_all(tag, **kwargs)
    matches = []
    for element in elements:
        if element.find(text=like(text)):
            matches.append(element)
    return matches
    #if len(matches) > 1:
    #    raise ValueError("Too many matches:\n" + "\n".join(matches))
    #elif len(matches) == 0:
    #    return None
    #else:
    #    return matches[0]

def parse_band(band):
    """
    Get the band info from the soup.
    """

    search_item = band.find_all("div")[2].find_all("div")
    info = {}
    info['band_name'] = search_item[1].text
    info['venue'] = search_item[2].text
    info['dtime'] = search_item[3].text
    info['num_interested'] = search_item[5].text
    return info

def get_bands(city,num_weeks):
    """
    Iterate through the bands and update.
    """
    urls = generate_urls_for_next_nweeks(city=city,num_weeks=num_weeks)
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    dfis = []
    for urli in urls:
        r = requests.get(urli, headers=header)
        soup = BeautifulSoup(r.text,features="lxml")
        bands = find_by_text(soup," PM","a")
        bandinfo = []
        for band in bands:
            bandinfo.append(parse_band(band))
        dfi = pd.DataFrame(bandinfo)
        dfis.append(dfi)

    return pd.concat(dfis,ignore_index=True).drop_duplicates(['band_name'])
