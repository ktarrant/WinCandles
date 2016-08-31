from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import date, timedelta
import pandas as pd


url_schedule = "http://www.retrosheet.org/schedule/{year}sked.txt"
def get_schedule(year):
	url = url_schedule.format(year=year)
	with urlopen(url) as webobj:
		return pd.read_csv(webobj, names=[
			'date', 'number', 'day',
			'away_team', 'away_league', 'away_gameid',
			'home_team', 'home_league', 'home_gameid',
			'time', 'event_reason', 'event_makeup',
			])

if __name__ == "__main__":
	print(get_schedule(2016))