import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os

summary_filename = os.path.join(".", "cache", "summary_WAS.csv")
summary = pd.DataFrame.from_csv(summary_filename)

app = dash.Dash()
available_intervals = ["HalfInning", "Inning", "Game"]
app.layout = html.Div([
    dcc.RadioItems(
        id='interval-dropdown',
        options=[{ 'label': k, 'value': k } for k in available_intervals],
        value='HalfInning'
        ),
    dcc.Graph(id='wincandle-history'),
])


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

def _make_team_fig(summary):
    # Figure out which halfInnings represent new games
    new_games = summary[summary.shift(-1)["Date"] != summary["Date"]]

    #colors = TEAM_COLORS_LOOKUP[team_name]
    return ({
            "x": summary.index,
            "open":summary.Open_WE50,
            "high":summary.Max_WE50,
            "low":summary.Min_WE50,
            "close":summary.Close_WE50,
            # "decreasing": {"line": {"color": colors[0]}},
            # "increasing": {"line": {"color": colors[1]}},
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

def collapse_bars(df):
    r_open = df.Open_WE50.iloc[0]
    r_close = df.Close_WE50.iloc[-1]
    r_high = df.Max_WE50.max()
    r_low = df.Min_WE50.min()


@app.callback(
     dash.dependencies.Output('wincandle-history', 'figure'),
     [dash.dependencies.Input('interval-dropdown', 'value')])
def make_team_summary(selected_interval):
    (trace, layout) = _make_team_fig()



    data = [trace]
    layout.update({
        'title': '{} Accumulated Win Expectency'.format("Team"),
        'yaxis': {'title': 'Wins above .500'},
        'xaxis1': {'title': 'Half-Innings', 'domain': [summary.index[0], summary.index[-1]]},
        'showlegend': False,
    })
    return dict(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server()