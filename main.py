import os
from collections import OrderedDict
import logging
from datetime import date
import pandas as pd
    
# Project-level imports
from urls import FANGRAPHS_NAME_REVERSE_REMAP
from schedule import get_mlb_schedule
from playlog import make_team_summary
from plot_summary import make_plotly_summary

log = logging.getLogger(__name__)

def _generate_plot_summaries(begin_date, cachedir):
    os.makedirs(cachedir, exist_ok=True)
    SCHEDULE_PATH = os.path.join(cachedir, "schedule.csv")

    log.debug("Loading schedule with begin date: {}".format(begin_date))
    try:
        schedule = pd.DataFrame.from_csv(SCHEDULE_PATH)
        log.info("Used cached schedule: {}".format(SCHEDULE_PATH))
    except IOError:
        schedule = get_mlb_schedule(begin_date)
        log.info("Loaded schedule: {}".format(schedule))
    schedule.to_csv(SCHEDULE_PATH)

    for team in sorted(FANGRAPHS_NAME_REVERSE_REMAP):
        # Generate a summary for each team from the playlog data
        log.info("Creating summary for team: {}".format(team))
        summary_path = os.path.join(cachedir, "summary_{}.csv".format(team))
        try:
            summary =  pd.DataFrame.from_csv(summary_path)
            log.info("Found cached schedule: {}".format(summary_path))
        except IOError:
            make_team_summary(SCHEDULE_PATH, team, summary_path)

        # Generate a plotly chart for each summary
        log.info("Creating summary for team: {}".format(team))
        yield (team, make_plotly_summary(team, summary_path, auto_open=False))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Creates the reddit comment with all the links.")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--cachedir", default="./cache")
    parser.add_argument("--output", default="comment.txt")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Collect the schedule for the month of may
    begin_date = date(year=2017, month=5, day=1)
    with open(args.output, "w") as fobj:
        for team, plotly_url in _generate_plot_summaries(begin_date, args.cachedir):
            fobj.write("{}: {}".format(team, plotly_url))

