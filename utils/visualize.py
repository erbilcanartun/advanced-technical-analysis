from bokeh.models import LinearAxis, Range1d
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.io import output_notebook, reset_output

import matplotlib.pyplot as plt

import numpy
import talib

from scipy.spatial.distance import pdist


def indicator_plot(ticker, price_data_series, price_data_frame, indicator_name, indicator_data, interactive=True, inline=True, fig_width = 1200, fig_height = 500):

    if interactive:
        interactive_plot(ticker, price_data_frame, indicator_name, indicator_data, inline = inline, fig_width = fig_width, fig_height = fig_height)
    else:
        static_plot(ticker, price_data_series, indicator_name, indicator_data)

    return None

def static_plot(ticker, price_data, indicator_name, indicator_data):

    fig, ax = plt.subplots(figsize=(13, 6))
    plt.style.use('classic')
    fig.set_facecolor('white')
    lw, fs = 1, 14
    plt.rc('lines', linewidth=lw)
    plt.rc('axes', linewidth=lw)
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams.update({'mathtext.default':'regular'})

    ax.plot(price_data, ls='-',color='blue', lw=.7)
    ax.tick_params(axis="x", direction="in", labelcolor='black', width=lw, length=4)
    ax.tick_params(axis="y", direction="in", labelcolor='blue', width=lw, length=4)
    ax.set_xlabel("Date", fontsize=fs, )
    ax.set_ylabel(ticker, fontsize=fs)

    ax_indicator = ax.twinx()
    ax_indicator.plot(indicator_data.indicator, color='green', lw=.8)
    ax_indicator.tick_params(axis="both", direction="in", left=True, labelcolor='green', width=lw, length=4)
    ax_indicator.set_ylabel(indicator_name, fontsize=fs)
    plt.show()
    return None

def interactive_plot(ticker, price_data, indicator_name, indicator_data, inline = True, fig_width = 1200, fig_height = 500):

    fs = '12pt'

    if inline:
        reset_output()
        output_notebook(notebook_type='jupyter', hide_banner=True)
    else:
        reset_output()
        output_file("candle_chart.html")

    # Increasing and decreasing candles
    inc = price_data.Close > price_data.Open
    dec = price_data.Open > price_data.Close

    # Candlestick width
    # candle_body_width = Half of the trading time in miliseconds
    candle_body_width = (price_data.index[1] - price_data.index[0]).total_seconds() * 1000 / 2

    # Prepare the candlestick chart
    tools = "pan, wheel_zoom, reset"
    candChart = figure(title="Price Chart", x_axis_type="datetime", tools=tools,
                       toolbar_location="right", toolbar_sticky=False,
                       width=fig_width, height=fig_height)
    # Green bars
    candChart.segment(x0=price_data.index[inc], y0=price_data.High[inc],
                      x1=price_data.index[inc], y1=price_data.Low[inc], color="green")
    candChart.vbar(x=price_data.index[inc], bottom=price_data.Open[inc],
                   top=price_data.Close[inc], width=candle_body_width,
                   fill_color="green", line_color="green")
    # Red bars
    candChart.segment(x0=price_data.index[dec], y0=price_data.High[dec],
                      x1=price_data.index[dec], y1=price_data.Low[dec], color="red")
    candChart.vbar(x=price_data.index[dec], bottom=price_data.Close[dec],
                   top=price_data.Open[dec], width=candle_body_width,
                   fill_color="red", line_color="red")

    # Set the axis labels
    #candChart.xaxis.axis_label = "Date"
    candChart.xaxis.axis_label_text_font_size = fs
    candChart.xaxis.axis_label_text_font_style = 'normal'
    #candChart.xaxis.axis_label_text_font = "times"
    #candChart.xaxis.axis_label_text_color = "black"

    candChart.yaxis.axis_label = ticker
    candChart.yaxis.axis_label_text_font_size = fs
    candChart.yaxis.axis_label_text_font_style = 'normal'
    #candChart.yaxis.axis_label_text_font = "times"
    #candChart.yaxis.axis_label_text_color = "black"

    #=============================== VOLUME CHART ================================#
    #volChart = figure(x_axis_type="datetime", width=fig_width, height=200)
    #volChart.vbar(dataframe.index[inc], width=width, top=dataframe.Volume[inc], fill_color="green", line_color="green", alpha=0.8)
    #volChart.vbar(dataframe.index[dec], width=width, top=dataframe.Volume[dec], fill_color="red", line_color="red", alpha=0.8)
    #volChart.xaxis.axis_label="Date"
    #volChart.yaxis.axis_label="Volume"

    #============================== INDICATOR CHART ==============================#
    indicatorChart = figure(title="Indicator Chart", x_axis_type="datetime", x_range=candChart.x_range,
                            tools=tools, toolbar_location="right", toolbar_sticky=False,
                            width=fig_width, height=300)
    indicatorChart.line(x=indicator_data.index, y=indicator_data.indicator, line_color="purple",
                        line_width=1.5, name=indicator_name, legend_label=indicator_name)

    indicatorChart.xaxis.axis_label="Date"
    indicatorChart.xaxis.axis_label_text_font_size = fs
    indicatorChart.xaxis.axis_label_text_font_style = 'normal'
    indicatorChart.yaxis.axis_label = indicator_name
    indicatorChart.yaxis.axis_label_text_font_size = fs
    indicatorChart.yaxis.axis_label_text_font_style = 'normal'

    indicatorChart.legend.location = "top_left"
    indicatorChart.legend.click_policy = "hide"

    layout = column(candChart, indicatorChart)
    show(layout)
    return None

def which_indicator(indicator_name:str):

    if indicator_name == 'SMA':
        return talib.SMA
    if indicator_name == 'EMA':
        return talib.EMA
    if indicator_name == 'RSI':
        return talib.RSI
    if indicator_name == 'STOCHRSI':
        return talib.STOCHRSI


def candle_chart(ticker, data,
                 indicators_on: dict = {'SMA':None, 'EMA':None},
                 indicators_off: dict = {'RSI':None, 'STOCHRSI':None},
                 inline=True, fig_width = 1200, fig_height = 500):

    if inline:
        reset_output()
        output_notebook(notebook_type='jupyter', hide_banner=True)
    else:
        reset_output()
        output_file("candle_chart.html")

    # Increasing and decreasing candles
    inc = data.Close > data.Open
    dec = data.Open > data.Close

    # Candlestick width
    # candle_body_width = Half of the trading time in miliseconds
    candle_body_width = (data.index[1] - data.index[0]).total_seconds() * 1000 / 2

    # Prepare the candlestick chart
    tools = "pan, wheel_zoom, reset"
    candChart = figure(title="Candle Chart", x_axis_type="datetime", tools=tools,
                       toolbar_location="right", toolbar_sticky=False,
                       width=fig_width, height=fig_height)
    # Green bars
    candChart.segment(x0=data.index[inc], y0=data.High[inc],
                      x1=data.index[inc], y1=data.Low[inc], color="green")
    candChart.vbar(x=data.index[inc], bottom=data.Open[inc],
                   top=data.Close[inc], width=candle_body_width,
                   fill_color="green", line_color="green")
    # Red bars
    candChart.segment(x0=data.index[dec], y0=data.High[dec],
                      x1=data.index[dec], y1=data.Low[dec], color="red")
    candChart.vbar(x=data.index[dec], bottom=data.Close[dec],
                   top=data.Open[dec], width=candle_body_width,
                   fill_color="red", line_color="red")

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
    if indicators_on:
        for key, value in indicators_on.items():
            if value != None:
                func = which_indicator(key)
                color = value[1]
                candChart.line(x=data.index, y=func(data["Close"], timeperiod=value[0]),
                               line_color=color, line_width=1.5, legend_label=key)

        candChart.legend.location = "top_left"
        candChart.legend.click_policy = "hide"

        layout = column(candChart)

    # Prepare the indicator chart that will be plotted below the main chart
    if indicators_off:

        indicatorChart = figure(x_axis_type="datetime", tools=tools, toolbar_location="right",
                                x_range=candChart.x_range, width=fig_width, height=300)

        dict_list = list(indicators_off.items())

        key = dict_list[0][0]
        value = dict_list[0][1]
        indicator = which_indicator(key)
        indicatorChart.line(data.index, indicator(data["Close"], timeperiod=value),
                            line_color='black', line_width=1.5, legend_label=key)
        # Set the axis labels for the first indicator
        indicatorChart.xaxis.axis_label = "Date"
        indicatorChart.yaxis.axis_label = key

        # Extra y-axis for the second indicator
        key = dict_list[1][0]
        value = dict_list[1][1]
        indicator = which_indicator(key)
        indicatorChart.extra_y_ranges = {key: Range1d()}
        indicatorChart.add_layout(LinearAxis(y_range_name=key, axis_label=key,
                                             major_label_text_color="blue",
                                             axis_label_text_color='orange'), 'right')

        fastk, fastd = indicator(data.Close, timeperiod=value,
                                 fastk_period=5, fastd_period=3, fastd_matype=0)
        indicatorChart.line(data.index, fastk, line_color="blue", line_width=1.5, legend_label=key)
        indicatorChart.line(data.index, fastd, line_color="orange", line_width=1.5, legend_label=key)

        indicatorChart.legend.location = "top_left"
        indicatorChart.legend.click_policy = "hide"

        layout = column(candChart, indicatorChart)

    show(layout)

    return None