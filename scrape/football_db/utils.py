#!/usr/bin/env python3
from itertools import chain
import numpy as np

from .constants import HEADERS

def validate_season(season_from, season_to, valid_seasons):

    if season_from > season_to:
        raise Exception('Season From must be less than or equal to Season To')

    if season_from not in valid_seasons:
        raise Exception('Season From {} is out of scope of the valid seasons for this site: {}'.format(
            season_from, valid_seasons))

    if season_to not in valid_seasons:
        raise Exception('Season To {} is out of scope of the valid seasons for this site: {}'.format(
            season_to, valid_seasons))


def validate_week(week_from, week_to):

    if week_from > week_to:
        raise Exception('Week From must be less than or equal to Week To')

    if not 1 <= week_from <= 17:
        raise Exception('Week From must be between 1 & 17 (inclusive)')

    if not 1 <= week_to <= 17:
        raise Exception('Week To must be between 1 & 17 (inclusive)')


def game_parameters_validator(season_from, season_to, week_from, week_to):

    # config = {'dk': [2014, 2015, 2016, 2017, 2018, 2019, 2020],
    #           'fd': [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    #           'yh': [2016, 2017, 2018, 2019, 2020]}

    # valid_season_numbers = config.get(dfs_site)
    valid_season_numbers = range(2010, 2021)

    # if not valid_season_numbers:  # unable to find the key
    #     raise Exception('Invalid dfs site')

    validate_season(season_from=season_from, 
                    season_to=season_to,
                    valid_seasons=valid_season_numbers)

    validate_week(week_from=week_from, week_to=week_to)

def parse_cols(url):
    response = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(response)
    table = soup.find('table', {'class': 'statistics scrollable'})
    table_data = table.find_all("tr")
    
    cols_lev1_str = [x.text for x in table_data[0].find_all("th")]
    cols_lev1_span = [x.attrs['colspan'] for x in table_data[0].find_all("th")]
    cols_lev1_nested = [[s]*int(cols_lev1_span[i]) for i, s in enumerate(cols_lev1_str)]
    cols_level1 = list(chain(*cols_lev1_nested))

    cols_level2 = [x.text for x in table_data[1].find_all("th")]

    cols = []
    for i, col in enumerate(cols_level2):
        prefix = cols_level1[i]
        if prefix == '\xa0':
            new_col = col
        else:
            new_col = f"{prefix}_{col}"
        cols.append(new_col)
    
    return cols