from schedule import get_schedule
from playlog import get_play_logs, get_play_log_data
from datetime import datetime
import logging

log = logging.getLogger(__name__)

def generate_play_logs(teamid, year=2016):
	sched = get_schedule(year)
	games = sched[(sched.home_team == teamid) | (sched.away_team == teamid)]
	for i in games.index:
		game = games.loc[i]
		game_date = datetime.strptime(str(game.date), '%Y%m%d').date()
		play_logs = get_play_logs(game_date)
		try:
			url_play_log = play_logs[game.home_team]
		except KeyError as e:
			log.error(
				"KeyError: Failed to find expected '{}' in Play Log list @ {}"
				.format(teamid, game_date))
			continue
		yield { 'date': game.date, 'home': teamid, 'away': game.away_team,
				'log': get_play_log_data(url_play_log) }

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	print(list(generate_play_logs('WAS')))