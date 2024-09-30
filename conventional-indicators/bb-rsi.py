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
    end_date = '2021-01-01'
    data = yf.download(ticker, start=start_date, end=end_date)

    # Increasing and decreasing candles
    inc = data.Close > data.Open
    dec = data.Open > data.Close

    # Candlestick width
    candle_body_width = (data.index[1] - data.index[0]).total_seconds() * 1000 / 2 # Half of the trading time in miliseconds
    fig_width = 1800
    fig_height = 500
    tools = "pan, wheel_zoom, reset"

    # Prepare the candlestick chart
    candChart = figure(x_axis_type="datetime", tools=tools, toolbar_location="right", width=fig_width, height=fig_height, title=ticker)
    # Green bars
    candChart.segment(x0=data.index[inc], y0=data.High[inc], x1=data.index[inc], y1=data.Low[inc], color="green")
    candChart.vbar(x=data.index[inc], bottom=data.Open[inc], top=data.Close[inc], width=candle_body_width, fill_color="green", line_color="green")
    # Red bars
    candChart.segment(x0=data.index[dec], y0=data.High[dec], x1=data.index[dec], y1=data.Low[dec], color="red")
    candChart.vbar(x=data.index[dec], bottom=data.Close[dec], top=data.Open[dec], width=candle_body_width, fill_color="red", line_color="red")

    candChart.title.text_font_size = "16pt"
    candChart.title.text_font_style = "bold"
    candChart.yaxis.axis_label = "USD"

    # Indicators that are plotted on the main chart
    # Bolinger Bands
    upperband, middleband, lowerband = ta.BBANDS(real=data.Close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    banddates = np.append(data.index, data.index[::-1])
    bandprice = np.append(lowerband, upperband[::-1])
    candChart.patch(pd.to_datetime(banddates), bandprice, color="#A6CEE3", fill_alpha=0.2, legend_label="BBANDS")

    candChart.legend.location = "top_left"
    candChart.legend.click_policy = "hide"

    # Prepare the indicator chart that will be plotted below the main chart
    indicatorChart = figure(x_axis_type="datetime", tools=tools, toolbar_location="right", x_range=candChart.x_range, width=fig_width, height=300)
    fastk, fastd = ta.STOCHRSI(data.Close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    indicatorChart.line(data.index, fastk, line_color="blue", line_width=1.5, legend_label="Stoch-RSI")
    indicatorChart.line(data.index, fastd, line_color="orange", line_width=1.5, legend_label="Stoch-RSI")
    # Set the axis labels
    indicatorChart.xaxis.axis_label = "Date"
    indicatorChart.yaxis.axis_label = "Stoch-RSI"
    # Extra y-axis for RSI
    indicatorChart.extra_y_ranges = {"rsi": Range1d()}
    indicatorChart.add_layout(LinearAxis(y_range_name="rsi", axis_label="RSI", major_label_text_color="green", axis_label_text_color='green'), 'right')
    indicatorChart.line(data.index, ta.RSI(data["Close"], timeperiod=14), line_color="green", line_width=1.5, legend_label="RSI")

    indicatorChart.legend.location = "top_left"
    indicatorChart.legend.click_policy = "hide"

    layout = column(candChart, indicatorChart)
    show(layout)


if __name__ == "__main__":
    main()