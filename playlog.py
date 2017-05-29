from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date, timedelta
import logging
import pandas as pd

# Project-level imports
from urls import FANGRAPHS_PLAYLOG_URL, FANGRAPHS_NAME_REVERSE_REMAP


log = logging.getLogger(__name__)


def get_playlog_data(url):
    log.info("Loading play log from url: {}".format(url))
    with urlopen(url) as webobj:
        soup = BeautifulSoup(webobj.read(), 'lxml')
    play_table = soup.find('table', {'class': 'rgMasterTable'})
    if play_table is None:
        raise ValueError("Play log missing: '{}'".format(url))
    table_headers = play_table.findAll('th', {'class': 'rgHeader'})
    clean_headers = [ td.text.strip() for td in table_headers ]
    table_entries = play_table.findAll('tr', {'class': ['rgRow', 'rgAltRow']})
    _clean = lambda s: s.strip().replace("%", "")
    raw_df = pd.DataFrame([
        { header: _clean(td.text) for header, td in zip(clean_headers, row.findAll('td')) }
        for row in table_entries
        ])
    return raw_df.apply(pd.to_numeric, errors='ignore')

def convert_playlog_to_summary(playlog):
    playlog["HalfInning"] = (playlog["Inn."] - 1) * 2 + playlog["Half"]
    playlog["WE50"] = (playlog["WE"] - 50.0) / 50.0
    entry_count = len(playlog.index)
    close_values = playlog[playlog["HalfInning"].shift(-1) != playlog["HalfInning"]].set_index("HalfInning")
    # Make open values from the close values. Set the first open value to 0 as that is game start
    open_values = close_values.shift(1)
    open_values["WE50"].iloc[0] = 0
    min_values = playlog.pivot_table(index="HalfInning", aggfunc=min)
    max_values = playlog.pivot_table(index="HalfInning", aggfunc=max)
    summary = pd.concat([
        open_values["WE50"],
        close_values["WE50"],
        min_values["WE50"],
        max_values["WE50"],
        max_values["LI"],
        ],
        axis=1, 
        keys=["Open_WE50", "Close_WE50", "Min_WE50", "Max_WE50", "Max_LI"])
    return summary

def summarize_team_from_schedule(schedule, team):
    last_date = None
    dh = 0
    for i in schedule.index:
        game = schedule.loc[i]
        if game.home_team != team and game.away_team != team:
            # This game isn't relevant to our search
            continue

        if last_date is None or last_date != game.date:
            last_date = game.date
            dh = 0
        else:
            if dh == 0:
                log.error("Detected there are two games on {} yet only one saved".format(game.date))
            elif dh == 1:
                log.info("Detected there are two games on {} and setting up second game".format(game.date))
                dh = 2
            else:
                raise ValueError("Detected 3 games in one day?? Is that possible??")

        fangraphs_name = FANGRAPHS_NAME_REVERSE_REMAP[game.home_team].replace(" ", "%20")
        try:
            playlog_url = FANGRAPHS_PLAYLOG_URL.format(date=game.date, team=fangraphs_name, dh=dh)
            playlog = get_playlog_data(playlog_url)
        except ValueError:
            log.debug("Failed to load date {} with dh=0, setting dh=1".format(game.date))
            dh = 1
            playlog_url = FANGRAPHS_PLAYLOG_URL.format(date=game.date, team=fangraphs_name, dh=dh)
            playlog = get_playlog_data(playlog_url)

        summary = convert_playlog_to_summary(playlog)
        if team == game.away_team:
            # Away team stats need to be negated
            summary["Open_WE50"] *= -1
            summary["Close_WE50"] *= -1
            summary["Min_WE50"] *= -1
            summary["Max_WE50"] *= -1

        entry_count = len(summary.index)
        summary["Date"] = [ game.date ] * entry_count
        opponent = game.away_team if team == game.home_team else game.home_team
        summary["Opponent"] = [ opponent ] * entry_count
        yield summary

def make_team_summary(source_csv, team, outfile):
    schedule = pd.DataFrame.from_csv(source_csv)
    total_summary = None
    for summary in summarize_team_from_schedule(schedule, team):
        if total_summary is None:
            total_summary = summary
        else:
            base_halfInning = max(total_summary.index) + 1
            base_WE50 = total_summary.iloc[-1]["Close_WE50"]
            log.debug("Using base_halfInning: {}".format(base_halfInning))
            log.debug("Using base_WE50: {}".format(base_WE50))
            summary.index = [i + base_halfInning for i in summary.index]
            summary["Open_WE50"] += base_WE50
            summary["Close_WE50"] += base_WE50
            summary["Min_WE50"] += base_WE50
            summary["Max_WE50"] += base_WE50
            total_summary = pd.concat([total_summary, summary])

    total_summary.to_csv(outfile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Loads summary for a team using play logs")
    parser.add_argument("team")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--source", default="schedule.csv")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    make_team_summary(args.source, args.team, "summary_{}.csv".format(team))

    