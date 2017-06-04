import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

# Project-level imports
from team_colors import TEAM_COLORS_LOOKUP

DIVISIONS = {
    "NLE": ["WAS", "NYN", "MIA", "ATL", "PHI"],
    "NLW": ["ARI", "LAN", "SFN", "COL", "SDN"],
    "NLC": ["CHN", "SLN", "PIT", "MIL", "CIN"],
    "ALE": ["BAL", "NYA", "BOS", "TBA", "TOR"],
    "ALW": ["HOU", "OAK", "SEA", "TEX", "ANA"],
    "ALC": ["DET", "CLE", "KCA", "MIN", "CHA"],
}

def _make_line_annot(index):
    return {
        'x0': index, 'x1': index,
        'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
        'line': {'color': 'rgb(30,30,30)', 'width': 1, 'dash': 'dot'},
    }

def _make_date_annot(index, date):
    return {
        'x': index, 'y': 0.05, 'xref': 'x', 'yref': 'paper',
        'showarrow': False, 'xanchor': 'left',
        'text': str(date)
    }

def _make_team_fig(team_name, summary):
    # Figure out which halfInnings represent new games
    new_games = summary[summary.shift(-1)["Date"] != summary["Date"]]

    colors = TEAM_COLORS_LOOKUP[team_name]
    return ({
            "x": summary.index,
            "open":summary.Open_WE50,
            "high":summary.Max_WE50,
            "low":summary.Min_WE50,
            "close":summary.Close_WE50,
            "decreasing": {"line": {"color": colors[0]}}, 
            "increasing": {"line": {"color": colors[1]}}, 
            "line": {"color": 'rgba(31,119,180,1)'}, 
            "type": 'candlestick', 
            "xaxis": 'x1', 
        },
        {
            "shapes": [ _make_line_annot(i) for i in new_games.index ],
            'annotations': [ _make_date_annot(i, summary["Date"].loc[i])
                for i in new_games.index[::4] ],
        }
    )

def make_team_summary(team_name, summary_filename, auto_open=True):
    summary = pd.DataFrame.from_csv(summary_filename)
    (trace, layout) = _make_team_fig(team_name, summary)

    data = [trace]
    layout.update({
        'title': '{} Accumulated Win Expectency'.format(team_name),
        'yaxis': {'title': 'Wins above .500'},
        'xaxis1': {'title': 'Half-Innings', 'domain': [summary.index[0], summary.index[-1]]},
        'showlegend': False,
    }) 
    fig = dict(data=data, layout=layout)
    url = py.plot(fig, filename='{}_winCandles'.format(team_name), auto_open=auto_open)
    return url

def make_division_summary(division_name, cachedir, auto_open=True):
    teams = DIVISIONS[division_name]
    data = []
    layout = {"shapes":[], "annotations":[]}
    for team in teams:
        summary_filename = os.path.join(args.cachedir, "summary_{}.csv".format(team))
        trace, this_layout = _make_team_fig(team, summary_filename)
        data += [ trace ]
        layout = { key: layout[key] + this_layout[key] for key in layout }
    layout.update({
        'title': '{} WE Accumulation Standings'.format(division_name),
        'yaxis': {'title': 'Wins above .500'},
        'xaxis1': {'title': 'Half-Innings', 'domain': [summary.index[0], summary.index[-1]]},
        'showlegend': False,
    })
    fig = dict(data=data, layout=layout)
    url = py.plot(fig, filename='{}_winCandles'.format(division_name), auto_open=auto_open)
    return url

if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Plots a summary for a team using play logs")
    parser.add_argument("--cachedir", default="./cache")
    subparsers = parser.add_subparsers(dest="command")
    team_parser = subparsers.add_parser('team')
    team_parser.add_argument("team")
    division_parser = subparsers.add_parser('division')
    division_parser.add_argument("division", choices=DIVISIONS.keys())
    args = parser.parse_args()

    print(args)
    if args.command == "division":
        make_division_summary(args.division, args.cachedir)
    elif args.command == "team":
        expected_filename = os.path.join(args.cachedir, "summary_{}.csv".format(args.team))
        make_team_summary(args.team, expected_filename)
    

