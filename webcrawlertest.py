from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame

ba_base_url = 'https://www.baseball-almanac.com'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def _parse_row_with_link(row):
    """take in a tr tag and get the data out of it in the form of a list of strings, also get box score link."""
    # parse the row like before and save it into a list
    parsed_row = [str(x.string) for x in row.find_all('td')]

    # now get the link
    # in a tag
    links = row.find_all('a')
    
    # opening day games < 1909 don't have box scores
    # in that case there's only one link (a tag) in the row, and we'll just
    # return our regular parsed row
    if len(links) < 2:
        return parsed_row
    else:
        link = links[0].get('herf') # note: starts with leading '../box-scores'
        full_link = ba_base_url + link[2:]
        return parsed_row + [full_link]
    
    
def scrape_opening_day_single_team_plus(team):
    team_response = requests.get(ba_base_url + f'/opening_day/odschedule.php?t={team}', headers=HEADERS)
    team_soup = Soup(team_response.text)

    tables = team_soup.find_all('table')

    team_table = tables[0]
    rows = team_table.find_all('tr')

    list_of_parsed_rows = [_parse_row_with_link(row) for row in rows[2:-2]]
    df = DataFrame(list_of_parsed_rows)
    df.columns = _parse_row(rows[1]) + ['boxscore_link']

    # let's add in team as a column
    df['team'] = team

    return df

""" this does not work
def time_and_place(url):
    if url is None:
        return""
    bs_reponse = request.get(url)
    bs_soup =Soup(bs_response.text)
    
    banner_tag = bs_soup.find('td', {'class': 'banner'})
    return st(banner_tag.text)
"""