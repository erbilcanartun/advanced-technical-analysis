from bokeh.models import LinearAxis, Range1d
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.io import output_notebook, reset_output

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy
import pandas
import talib

from scipy.spatial.distance import pdist


def indicator_plot(ticker, price, indicators, data_frame, volume_chart = False,
                   interactive = True, inline = True, fig_width = 1200, fig_height = 500):

    if interactive:
        return interactive_plot(ticker, price, indicators, data_frame, volume_chart,
                                inline, fig_width, fig_height)
    else:
        return static_plot(ticker, price, indicators, data_frame)

def static_plot(ticker, price, indicators, data_frame, inline = True):

    lw, fs = 1, 12
    within_price_scale = ['SMA', 'EMA', 'SAR', 'BB']
    colors = ['blue', 'orange', 'cyan', 'green', 'black', 'red', 'pink', 'brown']

    if inline:
        pass
    else:
        import matplotlib
        matplotlib.use('Qt5Agg')

    # Determine the number of additional indicators
    n_within_price = len([x for x in indicators if x in within_price_scale])
    n_additional = len(indicators) - n_within_price

    # Define the heights for each subplot
    heights = [4] + n_additional * [2]
    # Create a GridSpec layout
    gs = gridspec.GridSpec(nrows = n_additional + 1, ncols = 1, height_ratios = heights)

    # Create the figure
    fig = plt.figure(figsize=(10, sum(heights)), dpi=300)
    plt.style.use('classic')
    fig.set_facecolor('white')
    plt.rc('lines', linewidth=lw)
    plt.rc('axes', linewidth=lw)
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams.update({'mathtext.default':'regular'})

    # Price line on the first subplot
    ax = fig.add_subplot(gs[0])
    ax.plot(data_frame[price], ls='-', color='grey', lw=1.5, label=price)

    # Plot indicators on the primary y-axis
    for i, indicator in enumerate(indicators):
        if indicator in within_price_scale and indicator in data_frame.columns:
            ax.plot(data_frame[indicator], ls='-', color=colors[i], lw=lw, label=indicator)

    ax.set_ylabel(ticker, fontsize=fs)
    ax.tick_params(axis="both", direction="in", width=lw, length=4)
    ax.legend(loc='upper left', fontsize=fs * 0.8)

    if n_additional:
        indicators_additional = []
        for ind in indicators:
            if ind not in within_price_scale:
                indicators_additional.append(ind)

        # Plot additional indicators in separate subplots
        for i, indicator in enumerate(indicators_additional):
            j = n_within_price + i
            ax_additional = fig.add_subplot(gs[i + 1], sharex = ax)
            ax_additional.plot(data_frame[indicator], ls='-', color=colors[j], lw=lw, label=indicator)
            ax_additional.set_ylabel(indicator, fontsize=fs)
            ax_additional.tick_params(axis="both", direction="in", width=lw, length=4)
            ax_additional.legend(loc='upper left', fontsize=fs * 0.8)

        # Set the x-axis label for the last subplot
        ax_additional.set_xlabel("Date", fontsize=fs)
        ax.set_xticklabels([])
    else:
        ax.set_xlabel("Date", fontsize=fs)

    # Adjust layout
    plt.subplots_adjust(hspace=0)
    plt.show()
    return fig

def interactive_plot(ticker, price, indicators, data_frame, volume_chart,
                     inline = True, fig_width = 1200, fig_height = 500):
    lw = 1.5
    fs = '12pt'
    tools = "pan, wheel_zoom, box_zoom, reset, save"

    if inline:
        reset_output()
        output_notebook(notebook_type='jupyter', hide_banner=True)
    else:
        reset_output()
        output_file(f"{ticker}_chart.html")

    # Increasing and decreasing candles
    inc = data_frame.Close > data_frame.Open
    dec = data_frame.Open > data_frame.Close

    # Candlestick width
    # candle_body_width = Half of the trading time in miliseconds
    candle_body_width = (data_frame.index[1] - data_frame.index[0]).total_seconds() * 1000 / 2

    # Prepare the candlestick chart
    candChart = figure(title="Candlestick Chart", x_axis_type="datetime", tools=tools,
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
    candChart.xaxis.axis_label_text_font_size = fs
    candChart.xaxis.axis_label_text_font_style = 'normal'
    candChart.yaxis.axis_label = ticker
    candChart.yaxis.axis_label_text_font_size = fs
    candChart.yaxis.axis_label_text_font_style = 'normal'

    # VOLUME CHART
    if volume_chart:
        volChart = figure(title=None, x_axis_type="datetime",
                                       x_range=candChart.x_range, tools=tools,
                                       toolbar_location="right", toolbar_sticky=False,
                                       width=fig_width, height=200)
        volChart.vbar(data_frame.index[inc], width=fig_width, top=data_frame.Volume[inc],
                      fill_color="green", line_color="green", alpha=0.8)
        volChart.vbar(data_frame.index[dec], width=fig_width, top=data_frame.Volume[dec],
                      fill_color="red", line_color="red", alpha=0.8)
        volChart.yaxis.axis_label = "Volume"
        volChart.yaxis.axis_label_text_font_size = fs
        volChart.yaxis.axis_label_text_font_style = 'normal'

    # INDICATOR CHART
    within_price_scale = ['SMA', 'EMA', 'SAR', 'BB']
    colors = ['blue', 'orange', 'cyan', 'green', 'black', 'red', 'pink', 'brown']

    n = len([x for x in indicators if x in within_price_scale])

    # If all indicators will be on the main chart, don't initiate additional chart
    additional_chart = len(indicators) != n

    indicatorChart = [0 for _ in range(len(indicators))]
    for i, x in enumerate(indicators):

        if x in within_price_scale:
            if x == 'BB':
                # Bollinger Bands plot
                banddates = numpy.append(data_frame.index, data_frame.index[::-1])
                bandprice = numpy.append(data_frame['Lower_BB'], data_frame['Upper_BB'][::-1])
                candChart.patch(pandas.to_datetime(banddates), bandprice, color="#A6CEE3", fill_alpha=0.2, legend_label="BBANDS")

                # Other style
                #candChart.line(data_frame.index, data_frame['Middle_BB'], legend_label='Middle Band', line_color='black')
                #candChart.line(data_frame.index, data_frame['Upper_BB'], legend_label='Upper Band', line_color='red')
                #candChart.line(data_frame.index, data_frame['Lower_BB'], legend_label='Lower Band', line_color='red', line_dash='dashed')

            else:
                candChart.line(x=data_frame.index, y=data_frame[x], line_color=colors[i],
                               line_width=lw, name=x, legend_label=x)
            candChart.legend.location = "top_left"
            candChart.legend.click_policy = "hide"

        else:
            indicatorChart[i] = figure(title=None, x_axis_type="datetime",
                                       x_range=candChart.x_range, tools=tools,
                                       toolbar_location="right", toolbar_sticky=False,
                                       width=fig_width, height=300)
            if x == 'MACD':
                indicatorChart[i].line(data_frame.index, data_frame['MACD'], legend_label='MACD', line_color='blue')
                indicatorChart[i].line(data_frame.index, data_frame['MACD_signal'], legend_label='MACD Signal', line_color='orange')
                indicatorChart[i].vbar(data_frame.index, top=data_frame['MACD_hist'], width=0.5, color='green', legend_label='MACD Histogram')

            elif x == 'STOCH':
                indicatorChart[i].line(data_frame.index, data_frame['STOCH_k'], legend_label='STOCH_k', line_color='purple')
                indicatorChart[i].line(data_frame.index, data_frame['STOCH_d'], legend_label='STOCH_d', line_color='green')

            else:
                indicatorChart[i].line(x=data_frame.index, y=data_frame[x], line_color=colors[i],
                                       line_width=lw, name=x, legend_label=x)
            indicatorChart[i].xaxis.axis_label_text_font_size = fs
            indicatorChart[i].xaxis.axis_label_text_font_style = 'normal'
            indicatorChart[i].yaxis.axis_label = x
            indicatorChart[i].yaxis.axis_label_text_font_size = fs
            indicatorChart[i].yaxis.axis_label_text_font_style = 'normal'
            indicatorChart[i].legend.location = "top_left"
            indicatorChart[i].legend.click_policy = "hide"

    if additional_chart:
        indicator_chart_filtered = []
        for chart in indicatorChart:
            if chart and isinstance(chart, figure):
                indicator_chart_filtered.append(chart)
        indicator_chart_filtered[-1].xaxis.axis_label = "Date"

        if volume_chart:
            layout = column(candChart, volChart, *indicator_chart_filtered)
        else:
            layout = column(candChart, *indicator_chart_filtered)

    else:
        if volume_chart:
            volChart.xaxis.axis_label = "Date"
            layout = column(candChart, volChart)
        else:
            candChart.xaxis.axis_label = "Date"
            layout = column(candChart)

    show(layout)
    return layout