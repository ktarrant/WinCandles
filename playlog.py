from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import date, timedelta

url_root = "http://www.fangraphs.com/"
url_base = "{root}scoreboard.aspx?date={date}"
url_play = "{root}{log}"

def get_play_logs(date, root=url_root):
	url = url_base.format(root=root, date=date)
	with urlopen(url) as webobj:
		soup = BeautifulSoup(webobj.read(), 'lxml')

	play_log_soups = soup.findAll('a', text='Play Log')
	return [ url_play.format(root=url_root, log=s['href'])
		for s in play_log_soups ]

if __name__ == "__main__":
	test_date = date.today() - timedelta(days=1)
	play_logs = get_play_logs(test_date)
	print(play_logs)