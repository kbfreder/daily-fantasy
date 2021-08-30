#!/usr/bin/env python

import itertools
import regex as re
from io import StringIO
import time


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

from .utils import game_parameters_validator
from .constants import (
    BASE_URL,
    COLS,
    CURRENT_SEASON, 
    HEADERS,
    POS_DICT,
    # REGEX_PATTERN
)


# Function to create game search parameters
# def get_game_urls(season_from, week_from, season_to=None, week_to=None):
def get_game_data(season_from, week_from, season_to=None, week_to=None):
    """
    Returns game data

    Use this function to fetch NFL weekly player stats from footballdb.com

    Parameters
    ----------
    season_from: int
        The season number to begin search range.
    week_from: int
        The week of the season to begin search range
    season_to : int, default None
        The season number to search for data up to, inclusive.
    week_to : int, default None
        The week number to search for data up to, inclusive.


    Returns
    -------
    pd.DataFrame
        Data values include:
        =============   =======================================================
        gid             Unique id for each player (as `int`)
        week            The week number (as `int`)
        year            The season number (as `int`)
        player_name     Full player name, [Last Name, First Name] (as `str`)
        position        Player position, e.g. QB, TE, and Def (as `str`)
        team_name       Team the player is member of, abbreviation (as `str`)
        home_or_away    Identifies if a player was home or away (as `str`)
        opponent_name   Opponent name, abbreviation (as `str`)
        points          Total daily fantasy points scored (as `float`)
        salary          Daily fantasy salary, site specific (as `float`)
        dfs_site        Value indicating which dfs site the data relates to
        =======

    """
    season_to = season_to or season_from
    week_to = week_to or week_from

    # Ensure seasons are valid
    game_parameters_validator(season_from,
                              season_to=season_to,
                              week_from=week_from,
                              week_to=week_to)

    seasons = [*range(season_from, season_to + 1)]
    weeks = [*range(week_from, week_to + 1)]

    # season_urls = set([BASE_URL.format(s, w)
    #                    for s, w in itertools.product(seasons, weeks)
    #                    ])

    # return season_urls


    # Function to take game_urls and return data

    all_data = pd.DataFrame()

    # for url in game_urls:
    for yr, wk in itertools.product(seasons, weeks):
        print(f"Fetching season {yr}, week {wk}...")
        # (yr, wk) = re.search(REGEX_PATTERN, url).groups()
        # yr = int(yr)
        # wk = int(wk)
        for _, pos in POS_DICT.items():
            url = BASE_URL.format(pos, yr, wk)
            print(f"...position {pos}")

            response = requests.get(url, headers=HEADERS).text
            soup = BeautifulSoup(response, "lxml")

            table = soup.find('table', {'class': 'statistics scrollable'})
            table_data = table.find_all("tr")
            
            data_list = []
            for row in table_data[3:]:
                row_data = []
                row_td_list = row.find_all("td")
                for i, td in enumerate(row_td_list):
                    if i == 0:
                        s = td.find("a").text
                    else:
                        s = td.text
                    row_data.append(s)
                data_list.append(row_data)

            data_df = pd.DataFrame(data_list, columns=COLS)
            data_df['year'] = yr
            data_df['week'] = wk

            all_data = pd.concat(objs=[all_data, data_df])

            time.sleep(0.25)

    return all_data
