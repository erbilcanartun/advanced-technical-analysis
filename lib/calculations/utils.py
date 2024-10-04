import matplotlib.pyplot as plt
import numpy

def preprocess(time_series):

    series = (time_series - numpy.mean(time_series)) / numpy.std(time_series)
    series = 1 / (1 + numpy.exp(-numpy.array(series)))
    return series

def overview(ticker, price_data_series, period):

    series = preprocess(price_data_series)

    fig = plt.figure(constrained_layout=True, figsize=(11, 7))
    plt.style.use('classic')
    fig.set_facecolor('none')
    lw, fs = 2.5, 15
    plt.rc('lines', linewidth=lw)
    plt.rc('axes', linewidth=lw)
    plt.rcParams['font.family'] = 'Arial'

    gs = fig.add_gridspec(2, 1)
    ax1 = fig.add_subplot(gs[0, 0:])
    ax1.set_title(ticker + " Price Data", fontsize=fs, pad=15)
    ax1.plot(price_data_series, linestyle='-', marker='', markersize=10, color='darkblue')
    ax1.tick_params(axis="both", direction="in", left=True, width=lw, length=4, labelsize=fs)
    ax1.set_xlabel("Date", fontsize=fs)
    ax1.set_ylabel("Price", fontsize=fs)

    ax1 = fig.add_subplot(gs[1, 0:])
    ax1.set_title("\nDATA AFTER PREPROCESS", fontsize=fs, pad=15)
    ax1.plot(series, linestyle='-', marker='', markersize=10, color='lightblue')
    ax1.tick_params(axis="both", direction="in", left=True, width=lw, length=4, labelsize=fs)
    ax1.set_xlabel("Data Point Number", fontsize=fs)
    ax1.set_ylabel("Data [arb. unit]", fontsize=fs)
    plt.show()
    return fig