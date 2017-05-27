import re

MLB_URL_SCHEDULE = "http://m.mlb.com/schedule/{date.year:02}/{date.month:02}/{date.day:02}"

MLB_NAME_REMAP = {
    "Twins": "MIN",
    "Orioles": "BAL",
    "Blue Jays": "TOR",
    "Brewers": "MIL",
    "Marlins": "MIA",
    "Athletics": "SFA",
    "White Sox": "CHA",
    "D-backs": "ARI",
    "Reds": "CIN",
    "Indians": "CLE",
    "Rockies": "COL",
    "Phillies": "PHI",
    "Royals": "KCA",
    "Yankees": "NYA",
    "Mariners": "SEA",
    "Nationals": "WAS",
    "Angels": "ANA",
    "Rays": "TBA",
    "Padres": "SDN",
    "Mets": "NYN",
    "Rangers": "TEX",
    "Red Sox": "BOS",
    "Pirates": "PIT",
    "Braves": "ATL",
    "Giants": "SFN",
    "Cubs": "CHN",
    "Tigers": "DET",
    "Astros": "HOU",
    "Cardinals": "SLN",
    "Dodgers": "LAN",
}


FANGRAPHS_URL_ROOT = "http://www.fangraphs.com/"
FANGRAPHS_URL_BASE = "{root}scoreboard.aspx?date={date}"
FANGRAPHS_URL_PLAY = "{root}{log}"
FANGRAPHS_URL_TEAM_RE = re.compile(r"team=([\w\s]+)&")

FANGRAPHS_NAME_REMAP = {
    "Red Sox":      "BOS",
    "Indians":      "CLE",
    "Cubs":         "CHN",
    "Brewers":      "MIL",
    "Tigers":       "DET",
    "Orioles":      "BAL",
    "Royals":       "KCA",
    "Rangers":      "TEX",
    "Mets":         "NYN",
    "Angels":       "ANA",
    "Rockies":      "COL",
    "Astros":       "HOU",
    "Phillies":     "PHI",
    "Diamondbacks": "ARI",
    "Reds":         "CIN",
    "Yankees":      "NYA",
    "Nationals":    "WAS",
    "Athletics":    "SFA",
    "Giants":       "SFN",
    "Braves":       "ATL",
    "Rays":         "TBA",
    "Blue Jays":    "TOR",
    "Padres":       "SDN",
    "Marlins":      "MIA",
    "Pirates":      "PIT",
    "White Sox":    "CHA",
    "Mariners":     "SEA",
    "Cardinals":    "SLN",
    "Twins":        "MIN",
    "Dodgers":      "LAN",
}