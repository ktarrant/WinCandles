from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date, timedelta
import logging

log = logging.getLogger(__name__)


def get_play_log_data(url):
	log.debug("Loading play log from url: {}".format(url))
	return 0
	# TODO: Load play log data from play log url and retun
	# it to be concatenated all together

if __name__ == "__main__":
	test_date = date.today() - timedelta(days=3)
	play_logs = get_play_logs(test_date)
	print(play_logs)