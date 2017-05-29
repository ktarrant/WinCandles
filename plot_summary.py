import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

# Project-level imports
from team_colors import TEAM_COLORS_LOOKUP

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

def make_plotly_summary(team_name, summary_filename, auto_open=True):
    summary = pd.DataFrame.from_csv(summary_filename)
    # Figure out which halfInnings represent new games
    new_games = summary[summary.shift(-1)["Date"] != summary["Date"]]

    colors = TEAM_COLORS_LOOKUP[team_name]
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
        "xaxis": 'x1', 
    }

    data = [trace]
    layout = {
        'title': '{} Accumulated Win Expectency'.format(team_name),
        'yaxis': {'title': 'Wins above .500'},
        'xaxis1': {'title': 'Half-Innings', 'domain': [summary.index[0], summary.index[-1]]},
        'shapes': [ _make_line_annot(i) for i in new_games.index ],
        'annotations': [ _make_date_annot(i, summary["Date"].loc[i]) for i in new_games.index[::4] ],
        'showlegend': False,
    }
    fig = dict(data=data, layout=layout)
    url = py.plot(fig, filename='{}_winCandles'.format(team_name), auto_open=auto_open)
    return url

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plots a summary for a team using play logs")
    parser.add_argument("team")
    args = parser.parse_args()

    summary_filename = "summary_{}.csv".format(team_name)
    make_plotly_summary(args.team, summary_filename)
    

