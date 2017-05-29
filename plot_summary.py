import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

def _make_game_annot(index):
    return {
        'x0': index, 'x1': index,
        'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
        'line': {'color': 'rgb(30,30,30)', 'width': 1}
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

    trace = go.Candlestick(x=summary.index,
                           open=summary.Open_WE50,
                           high=summary.Max_WE50,
                           low=summary.Min_WE50,
                           close=summary.Close_WE50)
    data = [trace]
    layout = {
        'title': '{} Accumulated Win Expectency'.format(args.team),
        'yaxis': {'title': 'Wins above .500'},
        'xaxis': {'title': 'Half-Innings'}
        'shapes': game_annots,
        # 'annotations': [{
        #     'x': '2007-12-01', 'y': 0.05, 'xref': 'x', 'yref': 'paper',
        #     'showarrow': False, 'xanchor': 'left',
        #     'text': 'Official start of the recession'
        # }]
    }
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='{}_winCandles'.format(args.team))

