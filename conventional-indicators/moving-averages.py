from bokeh.layouts import column
from bokeh.plotting import figure, show
from bokeh.models import LinearAxis, Range1d

import talib as ta
import numpy as np
import pandas as pd
import yfinance as yf

def main():

    # Load financial data into a pandas DataFrame
    ticker = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2024-01-01'
    data = yf.download(ticker, start=start_date, end=end_date)

    # Increasing and decreasing candles
    inc = data.Close > data.Open
    dec = data.Open > data.Close

    # Candlestick width
    candle_body_width = (data.index[1] - data.index[0]).total_seconds() * 1000 / 2 # Half of the trading time in miliseconds
    fig_width = 1800
    tools = "pan, wheel_zoom, reset"

    # Prepare the candlestick chart
    candChart = figure(x_axis_type="datetime", tools=tools, toolbar_location="right", width=fig_width, height=800, title="Candle Chart")
    # Green bars
    candChart.segment(x0=data.index[inc], y0=data.High[inc], x1=data.index[inc], y1=data.Low[inc], color="green")
    candChart.vbar(x=data.index[inc], bottom=data.Open[inc], top=data.Close[inc], width=candle_body_width, fill_color="green", line_color="green")
    # Red bars
    candChart.segment(x0=data.index[dec], y0=data.High[dec], x1=data.index[dec], y1=data.Low[dec], color="red")
    candChart.vbar(x=data.index[dec], bottom=data.Close[dec], top=data.Open[dec], width=candle_body_width, fill_color="red", line_color="red")

    # Set the axis labels
    candChart.xaxis.axis_label = "Date"
    candChart.xaxis.axis_label_text_font_size = "14pt"
    candChart.xaxis.axis_label_text_font_style = "bold"
    #candChart.xaxis.axis_label_text_font = "times"
    candChart.xaxis.axis_label_text_color = "black"

    candChart.yaxis.axis_label = "AAPL-USD"
    candChart.yaxis.axis_label_text_font_size = "14pt"
    candChart.yaxis.axis_label_text_font_style = "bold"
    #candChart.yaxis.axis_label_text_font = "times"
    candChart.yaxis.axis_label_text_color = "black"

    # Indicators that are plotted on the main chart
    candChart.line(x=data.index, y=ta.SMA(data["Close"], timeperiod=9), line_color="blue", line_width=1.5, legend_label="SMA")
    candChart.line(x=data.index, y=ta.EMA(data["Close"], timeperiod=100), line_color="cyan", line_width=1.5, legend_label="EMA")

    candChart.legend.location = "top_left"
    candChart.legend.click_policy = "hide"

    layout = column(candChart)
    show(layout)


if __name__ == "__main__":
    main()