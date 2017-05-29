from urls import MLB_NAME_REMAP

TEAM_COLORS_RAW = {
    "Arizona D-backs": [ '#A71930', '#000000', 'E3D4AD'],
    "Atlanta Braves": [ '#CE1141', '#13274F'],
    "Baltimore Orioles": [ '#DF4601', '#000000'],
    "Boston Red Sox": [ '#BD3039', '#0D2B56'],
    "Chicago Cubs": [ '#CC3433', '#0E3386'],
    "Chicago White Sox": [ '#000000', '#C4CED4'],
    "Cincinnati Reds": [ '#C6011F', '#000000'],
    "Cleveland Indians": [ '#E31937', '#002B5C'],
    "Colorado Rockies": [ '#333366', '#231F20', 'C4CED4'],
    "Detroit Tigers": [ '#0C2C56', '#000000'],
    "Houston Astros": [ '#002D62', '#EB6E1F'],
    "Kansas City Royals": [ '#004687', '#C09A5B'],
    "Los Angeles Angels of Anaheim": [ '#BA0021', '#003263'],
    "Los Angeles Dodgers": [ '#EF3E42', '#005A9C'],
    "Miami Marlins": [ '#FF6600', '#0077C8', 'FFD100', '000000'], 
    "Milwaukee Brewers": [ '#0A2351', '#B6922E'],
    "Minnesota Twins": [ '#002B5C', '#D31145'],
    "New York Mets": [ '#FF5910', '#002D72'],
    "New York Yankees": [ '#E4002B', '#003087'],
    "Oakland Athletics": [ '#003831', '#EFB21E'],
    "Philadelphia Phillies": [ '#284898', '#E81828'],
    "Pittsburgh Pirates": [ '#FDB827', '#000000'],
    "San Diego Padres": [ '#002D62', '#FEC325', '7F411C', 'A0AAB2'],
    "San Francisco Giants": [ '#FD5A1E', '#000000', '8B6F4E'],
    "Seattle Mariners": [ '#0C2C56', '#005C5C', 'C4CED4'],
    "St Louis Cardinals": [ '#C41E3A', '#000066', 'FEDB00'],
    "Tampa Bay Rays": [ '#092C5C', '#8FBCE6', 'F5D130'],
    "Texas Rangers": [ '#C0111F', '#003278'],
    "Toronto Blue Jays": [ '#134A8E', '#1D2D5C', 'E8291C'],
    "Washington Nationals": [ '#AB0003', '#11225B'],
}

def _find_team_id(team_name):
    for mlb_name in MLB_NAME_REMAP:
        if mlb_name in team_name:
            return MLB_NAME_REMAP[mlb_name]
    raise KeyError("Failed to find team id for: {}".format(team_name))
TEAM_COLORS_LOOKUP = { _find_team_id(team_name): TEAM_COLORS_RAW[team_name]
    for team_name in TEAM_COLORS_RAW}