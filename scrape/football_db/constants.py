CURRENT_SEASON = 2021
# CURRENT_SEASON_BASE_URL = 
BASE_URL = "https://www.footballdb.com/fantasy-football/index.html?pos={}&yr={}&wk={}&rules=2"
# PREVIOUS_SEASON_BASE_URL = ∫

POS_DICT = {
    # 'all_offense': 'QB%2CRB%2CWR%2CTE',
    'QB': 'QB',
    'RB': 'RB',
    'WR': 'WR', 
    'TE': 'TE',
    # 'Def': 'DST',
}

# extract season (year) and week from URL
REGEX_PATTERN = "yr=([0-9]{4})&wk=([0-9]{1,2})"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

COLS = [
    'Player',
    'Game',
    'Pts*',
    'Passing_Att',
    'Passing_Cmp',
    'Passing_Yds',
    'Passing_TD',
    'Passing_Int',
    'Passing_2Pt',
    'Rushing_Att',
    'Rushing_Yds',
    'Rushing_TD',
    'Rushing_2Pt',
    'Receiving_Rec',
    'Receiving_Yds',
    'Receiving_TD',
    'Receiving_2Pt',
    'Fumbles_FL',
    'Fumbles_TD'
    ]