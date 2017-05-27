from datetime import date, timedelta
import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Project-level imports
from urls import *

# ==================================================================================================
# MLB.COM SCHEDULE DOWNLOADER
# ==================================================================================================

def split_mlb_schedule_result(schedule_result, key_remap=MLB_NAME_REMAP):
    if "," in schedule_result:
        results = schedule_result.split(", ")
        result1 = results[0].split(" ")
        result2 = results[1].split(" ")
        return {
            "away_team": key_remap[" ".join(result1[:-1])],
            "away_score": int(result1[-1]),
            "home_team": key_remap[" ".join(result2[:-1])],
            "home_score": int(result2[-1]),
            }

    elif "@" in schedule_result:
        # this game is still in progress
        mid_result = schedule_result.split(" @ ")
        return {
             "home_team": key_remap[mid_result[0]],
             "home_score": 0,
             "away_team": key_remap[mid_result[1]],
             "away_score": 0,
             }
    

def get_mlb_schedule(schedule_date):
    url = MLB_URL_SCHEDULE.format(date=schedule_date)
    print("loading url: {}".format(url))
    with urlopen(url) as webobj:
        soup = BeautifulSoup(webobj, "lxml")
        first_table = soup.find('table', {'class': 'schedule-list'})
        matchup_columns = first_table.findAll('td', {'class': 'schedule-matchup'})
        text_results = [ td.text for td in matchup_columns ]
        return [ split_mlb_schedule_result(text) for text in text_results ]


# ==================================================================================================
# FANGRAPHS GAME DAY LINK DOWNLOADER
# ==================================================================================================

def get_play_logs(date, root=FANGRAPHS_URL_ROOT, key_remap=FANGRAPHS_NAME_REMAP):
    url = FANGRAPHS_URL_BASE.format(root=root, date=date)
    with urlopen(url) as webobj:
        soup = BeautifulSoup(webobj.read(), 'lxml')

    play_log_soups = soup.findAll('a', text='Play Log')
    play_log_urls = [ FANGRAPHS_URL_PLAY.format(root=FANGRAPHS_URL_ROOT, log=s['href'])
        for s in play_log_soups ]
    if key_remap is not None:
        return { key_remap[FANGRAPHS_URL_TEAM_RE.findall(url)[0]] : url
            for url in play_log_urls }
    else:
        return { FANGRAPHS_URL_TEAM_RE.findall(url)[0] : url
            for url in play_log_urls }


if __name__ == "__main__":
    schedule_date = date.today() - timedelta(days=3)
    schedule = get_mlb_schedule(schedule_date)
    playlog = get_play_logs(schedule_date)
    for game in schedule:
        home_team = game['home_team']
        try:
            game['playlog_url'] = playlog[home_team]
        except KeyError:
            print("Failed to find team in playlog: {}".format(home_team))
            pprint.pprint(playlog)
            exit(1)

    df = pd.DataFrame(schedule)
    df.to_csv("schedule.csv")