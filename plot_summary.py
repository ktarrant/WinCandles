import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plots a summary for a team using play logs")
    parser.add_argument("team")
    args = parser.parse_args()

    summary_filename = "summary_{}.csv".format(args.team)
    summary = pd.DataFrame.from_csv(summary_filename)


    trace = go.Candlestick(x=summary.index,
                           open=summary.Open_WE50,
                           high=summary.Max_WE50,
                           low=summary.Min_WE50,
                           close=summary.Close_WE50)
    data = [trace]
    py.plot(data, filename='{}_winCandles'.format(args.team))