import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

# Project-level imports
from team_colors import TEAM_COLORS_LOOKUP

def _make_game_annot(index):
    return {
        'x0': index, 'x1': index,
        'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
        'line': {'color': 'rgb(30,30,30)', 'width': 1, 'dash': 'dot'},
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plots a summary for a team using play logs")
    parser.add_argument("team")
    args = parser.parse_args()

    summary_filename = "summary_{}.csv".format(args.team)
    summary = pd.DataFrame.from_csv(summary_filename)
    # Figure out which halfInnings represent new games
    new_games = summary[summary.shift(-1)["Date"] != summary["Date"]]
    game_annots = [ _make_game_annot(i) for i in new_games.index ]
    colors = TEAM_COLORS_LOOKUP[args.team]
    trace = {
        "x": summary.index,
        "open":summary.Open_WE50,
        "high":summary.Max_WE50,
        "low":summary.Min_WE50,
        "close":summary.Close_WE50,
        "decreasing": {"line": {"color": colors[0]}}, 
        "increasing": {"line": {"color": colors[1]}}, 
        "line": {"color": 'rgba(31,119,180,1)'}, 
        "type": 'candlestick', 
  # "xaxis": 'x', 
  # "yaxis": 'y'
    }

    data = [trace]
    layout = {
        'title': '{} Accumulated Win Expectency'.format(args.team),
        'yaxis': {'title': 'Wins above .500'},
        'xaxis': {'title': 'Half-Innings'},
        'shapes': game_annots,
        # 'annotations': [{
        #     'x': '2007-12-01', 'y': 0.05, 'xref': 'x', 'yref': 'paper',
        #     'showarrow': False, 'xanchor': 'left',
        #     'text': 'Official start of the recession'c
        # }]
    }
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='{}_winCandles_V2'.format(args.team))

