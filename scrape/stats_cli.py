#!/usr/bin/env python3
import click
from datetime import date

from football_db import games


# Options for command line interface
@click.command()
@click.option('--season_from',
              type=int,
              prompt='Season beginning',
              help='The season number in the beginning search range')
@click.option('--season_to',
              type=int,
              prompt='Season ending',
              help='The season number at the end of the search range (inclusive)')
@click.option('--week_from',
              type=int,
              prompt='Week beginning',
              help='The week number in the beginning search range')
@click.option('--week_to',
              type=int,
              prompt='Week ending',
              help='The week number at the end of the search range (inclusive)')
@click.option('--file_name_type',
              type=str,
              prompt='Filename',
              default='season',
              help="How to name datafile")
def main(season_from, season_to, week_from, week_to, file_name_type):
    """
    Simple program to scrape NFL daily fantasy points and salary information.
    Designed to be used as a bulk download tool. Results are returned in comma
    delimited format (csv) to the /data directory. Refer there to look at the
    'draftkings_sample_output.csv'.

    DFS_SITE The name of the dfs site to return data for. Refer to the package
    docs for more usage examples.

    """
    # g = games.find_games(season_from=season_from,
    #                     week_from=week_from,
    #                     season_to=season_to,
    #                     week_to=week_to)
    
    # data = games.get_game_data(game_urls=g)

    data = games.get_game_data(
        season_from=season_from,
        week_from=week_from,
        season_to=season_to,
        week_to=week_to
    )
    
    if file_name_type == 'date':
        file_name = date.today().strftime('%Y%m%d')
    else:
        if (week_from == 1) & (week_to == 17):
            file_name = f'{season_from}'
        else:
            file_name = f'{season_from}_weeks{week_from}-{week_to}'

    return data.to_csv(f'data/fbdb_{file_name}.csv')


if __name__ == "__main__":
    print('Welcome to NFL DFS!\n')
    main()
