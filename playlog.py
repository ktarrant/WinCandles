from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import date, timedelta
import logging

log = logging.getLogger(__name__)

url_root = "http://www.fangraphs.com/"
url_base = "{root}scoreboard.aspx?date={date}"
url_play = "{root}{log}"
url_team_re = re.compile(r"team=([\w\s]+)&")

NAME_REMAP = {
	"Red Sox":		"BOS",
	"Indians":		"CLE",
	"Cubs":			"CHN",
	"Brewers":		"MIL",
	"Tigers":		"DET",
	"Orioles":		"BAL",
	"Royals":		"KCA",
	"Rangers":		"TEX",
	"Mets":			"NYN",
	"Angels":		"ANA",
	"Rockies":		"COL",
	"Astros":		"HOU",
	"Phillies":		"PHI",
	"Diamondbacks":	"ARI",
	"Reds":			"CIN",
	"Yankees":		"NYA",
	"Nationals":	"WAS",
	"Athletics":	"SFA",
	"Giants":		"SFN",
	"Braves":		"ATL",
	"Rays":			"TBA",
	"Blue Jays":	"TOR",
	"Padres":		"SDN",
	"Marlins":		"MIA",
	"Pirates":		"PIT",
	"White Sox":	"CHA",
	"Mariners":		"SEA",
	"Cardinals":	"SLN",
	"Twins":		"MIN",
	"Dodgers":		"LAN",
}

def get_play_logs(date, root=url_root):
	url = url_base.format(root=root, date=date)
	with urlopen(url) as webobj:
		soup = BeautifulSoup(webobj.read(), 'lxml')

	play_log_soups = soup.findAll('a', text='Play Log')
	play_log_urls = [ url_play.format(root=url_root, log=s['href'])
		for s in play_log_soups ]
	return { NAME_REMAP[url_team_re.findall(url)[0]] : url
		for url in play_log_urls }

def get_play_log_data(url):
	log.debug("Loading play log from url: {}".format(url))
	return 0
	# TODO: Load play log data from play log url and retun
	# it to be concatenated all together

if __name__ == "__main__":
	test_date = date.today() - timedelta(days=1)
	play_logs = get_play_logs(test_date)
	print(play_logs)