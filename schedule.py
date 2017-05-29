from datetime import date, timedelta, datetime
import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import OrderedDict
import logging

# Project-level imports
from urls import *

log = logging.getLogger(__name__)

# ==================================================================================================
# MLB.COM SCHEDULE DOWNLOADER
# ==================================================================================================

def split_mlb_schedule_result(schedule_result, schedule_date, key_remap=MLB_NAME_REMAP):
    if "," in schedule_result:
        results = schedule_result.split(", ")
        result1 = results[0].split(" ")
        result2 = results[1].split(" ")
        return {
            "away_team": key_remap[" ".join(result1[:-1])],
            "away_score": int(result1[-1]),
            "home_team": key_remap[" ".join(result2[:-1])],
            "home_score": int(result2[-1]),
            "date": schedule_date,
            }

    elif "@" in schedule_result:
        # this game is still in progress
        mid_result = schedule_result.split(" @ ")
        return {
             "home_team": key_remap[mid_result[0]],
             "home_score": 0,
             "away_team": key_remap[mid_result[1]],
             "away_score": 0,
             "date": schedule_date,
             }

# Should match: Sunday, May 28, 2017 and return May 28, 2017
_mlb_date_re = re.compile("[A-Z][a-z]+, ([A-Z][a-z]+) ([0-9]+), ([0-9]{4})")

def _get_mlb_sched_by_url(url):
    log.info("loading url: {}".format(url))
    with urlopen(url) as webobj:
        soup = BeautifulSoup(webobj, "lxml")
        for schedule_module in soup.findAll('section', {'class': 'module'}):
            schedule_header = schedule_module.find('h4')
            header_match = _mlb_date_re.match(schedule_header.text)
            if header_match is None:
                continue
            header_date = datetime.strptime(" ".join(header_match.groups()), '%B %d %Y')
            schedule_table = schedule_module.find('table', {'class': 'schedule-list'})
            matchup_columns = schedule_table.findAll('td', {'class': 'schedule-matchup'})
            text_results = [ td.text for td in matchup_columns ]
            try:
                yield [ split_mlb_schedule_result(text, header_date.date())
                    for text in text_results ]
            except KeyError:
                continue

def get_mlb_schedule(start_date):
    """ Gets the MLB schedule from start_date up to today. """
    todays_schedule = [ game for game_list in _get_mlb_sched_by_url(MLB_URL_SCHEDULE_BASE)
        for game in game_list ]
    earliest_day = todays_schedule[0]["date"]
    while earliest_day > start_date:
        previous_set_day = earliest_day - timedelta(days=3)
        previous_set_url = MLB_URL_SCHEDULE_DATE.format(date=previous_set_day)
        # Tack the new game list onto the beginning because these are older games
        todays_schedule = [ game for game_list in _get_mlb_sched_by_url(previous_set_url)
            for game in game_list] + todays_schedule
        earliest_day = previous_set_day

    # url = MLB_URL_SCHEDULE.format(date=start_date)
    schedule_table = pd.DataFrame(todays_schedule)
    # filter out invalid date
    schedule_table = schedule_table[
        schedule_table["date"] >= start_date][schedule_table["date"] < date.today()]
    return schedule_table


# ==================================================================================================
# FANGRAPHS GAME DAY LINK DOWNLOADER
# ==================================================================================================

""" NOTE: Should no longer be needed. Remove? """
def get_play_logs(date, root=FANGRAPHS_URL_ROOT, key_remap=FANGRAPHS_NAME_REMAP):
    url = FANGRAPHS_URL_BASE.format(root=root, date=date)
    log.info("loading url: {}".format(url))
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
    logging.basicConfig(level=logging.INFO)
    # Collect the schedule for the month of may
    schedule = get_mlb_schedule(date(year=2017, month=4, day=2))
    print(schedule)
    schedule.to_csv("schedule.csv")