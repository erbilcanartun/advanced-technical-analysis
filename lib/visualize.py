from bokeh.models import LinearAxis, Range1d
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.io import output_notebook, reset_output

import matplotlib.pyplot as plt

import numpy
import talib

from scipy.spatial.distance import pdist


def indicator_plot(ticker, price, indicator, data_frame, indicator_where = 'on_price',
                   interactive = True, inline = True, fig_width = 1200, fig_height = 500):

    if interactive:
        return interactive_plot(ticker, price, indicator, data_frame, indicator_where,
                                inline, fig_width, fig_height)
    else:
        return static_plot(ticker, price_data_series, indicator_name, indicator_data)

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
    ax_indicator.plot(indicator_data[indicator_name], color='green', lw=.8)
    ax_indicator.tick_params(axis="both", direction="in", left=True,
                             labelcolor='green', width=lw, length=4)
    ax_indicator.set_ylabel(indicator_name, fontsize=fs)
    plt.show()
    return fig

def interactive_plot(ticker, price, indicator, data_frame,
                     indicator_where = 'on_price', inline = True,
                     fig_width = 1200, fig_height = 500):

    fs = '12pt'

    if inline:
        reset_output()
        output_notebook(notebook_type='jupyter', hide_banner=True)
    else:
        reset_output()
        output_file("candle_chart.html")

    # Increasing and decreasing candles
    inc = data_frame.Close > data_frame.Open
    dec = data_frame.Open > data_frame.Close

    # Candlestick width
    candle_body_width = (data_frame.index[1] - data_frame.index[0]).total_seconds() * 1000 / 2
    # candle_body_width = Half of the trading time in miliseconds

    # Prepare the candlestick chart
    tools = "pan, wheel_zoom, reset"
    candChart = figure(title="Price Chart", x_axis_type="datetime", tools=tools,
                       toolbar_location="right", toolbar_sticky=False,
                       width=fig_width, height=fig_height)
    # Green bars
    candChart.segment(x0=data_frame.index[inc], y0=data_frame.High[inc],
                      x1=data_frame.index[inc], y1=data_frame.Low[inc], color="green")
    candChart.vbar(x=data_frame.index[inc], bottom=data_frame.Open[inc],
                   top=data_frame.Close[inc], width=candle_body_width,
                   fill_color="green", line_color="green")
    # Red bars
    candChart.segment(x0=data_frame.index[dec], y0=data_frame.High[dec],
                      x1=data_frame.index[dec], y1=data_frame.Low[dec], color="red")
    candChart.vbar(x=data_frame.index[dec], bottom=data_frame.Close[dec],
                   top=data_frame.Open[dec], width=candle_body_width,
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
    #volChart.vbar(data_frame.index[inc], width=width, top=data_frame.Volume[inc], fill_color="green", line_color="green", alpha=0.8)
    #volChart.vbar(data_frame.index[dec], width=width, top=data_frame.Volume[dec], fill_color="red", line_color="red", alpha=0.8)
    #volChart.xaxis.axis_label="Date"
    #volChart.yaxis.axis_label="Volume"

    #============================== INDICATOR CHART ==============================#

    if indicator_where == 'on_price':

        for i, ind in enumerate(indicator):
            candChart.line(x=data_frame.index, y=data_frame[ind], line_color='purple',
                           line_width=1.5, name=ind, legend_label=ind)

        candChart.legend.location = "top_left"
        candChart.legend.click_policy = "hide"
        layout = column(candChart)

    elif indicator_where == 'below_price':

        indicatorChart = figure(title="Indicator Chart", x_axis_type="datetime",
                                x_range=candChart.x_range, tools=tools,
                                toolbar_location="right", toolbar_sticky=False,
                                width=fig_width, height=300)

        for i, ind in enumerate(indicator):

            indicatorChart.line(x=data_frame.index, y=data_frame[ind], #line_color="purple",
                                line_width=1.5, name=ind, legend_label=ind)

        indicatorChart.xaxis.axis_label="Date"
        indicatorChart.xaxis.axis_label_text_font_size = fs
        indicatorChart.xaxis.axis_label_text_font_style = 'normal'
        indicatorChart.yaxis.axis_label = ind
        indicatorChart.yaxis.axis_label_text_font_size = fs
        indicatorChart.yaxis.axis_label_text_font_style = 'normal'
        indicatorChart.legend.location = "top_left"
        indicatorChart.legend.click_policy = "hide"
        layout = column(candChart, indicatorChart)

    else:
        raise KeyError("Choose either of on_price or below_price options for indicator_where.")

    show(layout)
    return layout

def which_indicator(indicator_name:str):

    if indicator_name == 'SMA':
        return talib.SMA
    if indicator_name == 'EMA':
        return talib.EMA
    if indicator_name == 'RSI':
        return talib.RSI
    if indicator_name == 'STOCHRSI':
        return talib.STOCHRSI