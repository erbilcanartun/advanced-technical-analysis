import numpy
import pandas
from utils.salib import *

def preprocess(time_series):
    series = (time_series - numpy.mean(time_series)) / numpy.std(time_series)
    series = 1 / (1 + numpy.exp(-numpy.array(series)))
    return series

def overview(time_series, period):

    series = preprocess(time_series)

    fig = plt.figure(constrained_layout=True, figsize=(11, 7))
    plt.style.use('classic')
    fig.set_facecolor('none')
    lw, fs = 2.5, 15
    plt.rc('lines', linewidth=lw)
    plt.rc('axes', linewidth=lw)
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams.update({'mathtext.default':'regular'})

    gs = fig.add_gridspec(2, 1)
    ax1 = fig.add_subplot(gs[0, 0:])
    ax1.set_title(filename, fontsize=fs, pad=15)
    ax1.plot(time_series, linestyle='-', marker='', markersize=10, color='darkblue')
    ax1.tick_params(axis="both", direction="in", left=True, width=lw, length=4, labelsize=fs)
    ax1.set_xlabel(r"$Date$", fontsize=fs)
    #ax1.set_ylabel(PAIR_NAME, fontsize=fs)

    ax1 = fig.add_subplot(gs[1, 0:])
    ax1.set_title("DATA AFTER PREPROCESS", fontsize=fontsizes, pad=15)
    ax1.plot(series, linestyle='-', marker='', markersize=10, color='lightblue')
    ax1.tick_params(axis="both", direction="in", left=True, width=lw, length=4, labelsize=fs)
    ax1.set_xlabel(r"$Data \ Point \ Number$", fontsize=fs)
    ax1.set_ylabel(r"$Data \ [arb. unit]$", fontsize=fs)
    plt.show()

    return None

def sh_en(data: pandas.Series, period: int):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values
        se = Entropy.shannon(x)
        df.loc[df.index[t]] = [se]

        print("t = %d; Shannon entropy = %f" % (t, se), end='')
        print("\t\t\t", end='\r')

    return df

def ap_en(data: pd.Series, period: int):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values
        ae = Entropy.approximate(x, m=2, r=3)
        df.loc[df.index[t]] = [ae]

        print("t = %d; Approximate entropy = %f" % (t, ae), end='')
        print("\t\t\t", end='\r')

    return df

def lyapunov(data: pandas.Series, period: int):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values

        # Diameter selection
        diameter_set = 2 ** numpy.linspace(0, -50, 200) * 5

        for diameter in diameter_set:
            counter = 0
            for i in range(period):
                for j in range(i + 1, period):

                    if numpy.abs(x[i] - x[j]) <= diameter:
                        counter += 1
            if counter <= 15: break

        # Lyapunov exponent
        lyapunov = lyapunov_exponent(x, candle_range=period, initial_diameter=diameter, display=False)
        df.loc[df.index[t]] = [lyapunov]

        print("t = %d; Lyapunov exp. = %f" % (t, lyapunov), end='')
        print("\t\t\t", end='\r')

    return df

def minfo(data: pandas.Series, period: int, delay: int,
          max_delay: int, method: str = 'constant delay'):
    # Delay time (should be less than 'length')

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])

    if method == 'constant delay':

        print(f"Period = {period}\nData length = {N}\n")
        for t in range(period - 1 + delay, N):

            unlagged = data[t - (period - 1) - delay:t + 1 - delay].values
            lagged = data[t - (period - 1):t + 1].values

            info = mutual_info(unlagged, lagged, local=False)
            df.loc[df.index[t]] = [info]

            print("t = %d; Mutual info. = %f" % (t, info), end='')
            print("\t\t\t", end='\r')

    elif method == 'first minimum':

        print(f"Period = {period}\nData length = {N}\n")

        for t in range(period - 1, N):

            x = data[t - (period - 1):t + 1].values
            information = []
            for tau in range(1, max_delay + 1):

                unlagged = x[:-tau]
                lagged = numpy.roll(x, -tau)[:-tau]

                if len(unlagged):

                    info = mutual_info(unlagged, lagged, local=False)
                    information.append(info)

                    print("t = %d; tau = %d; mutual information = %.5f" % (t, tau, info), end='')
                    print("\t\t\t", end='\r')

                    if len(information) > 1 and information[-2] < information[-1]: # First local minimum
                        first_minimum = tau - 1
                        df.loc[df.index[t]] = [first_minimum]
                        break
                    #else:
                    #    first_minimum = min(information)
                    #    df.loc[df.index[t]] = [first_minimum]

    else:
        raise ValueError

    return df

def complex(data: pandas.Series, period: int):

    df = pd.DataFrame(index=dataframe.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values
        binary_sequence = Complexity.binarizer(x)
        complexity = Complexity.lempel_ziv_complexity(np.array(binary_sequence))
        df.loc[df.index[t]] = [complexity]

        print("t = %d; Lempel-Ziv complexity = %f" % (t, complexity), end='')
        print("\t\t\t", end='\r')

    return df

def mfa(data, period, q_range = (-40, 40), scale_range = (1, 7)):

    series = preprocess(data)

    q_values = np.arange(q_range[0], q_range[1] + 1)
    scale_values = np.arange(scale_range[0], scale_range[1] + 1)


    #---------------- CHHABRA-JENSEN CALCULATION ----------------#
    results = chhabra_jensen_analysis(series[:L], q_values, scale_values) # output: [alpha, falpha, Dq, Rsquared_alpha, Rsquared_falpha, Rsquared_Dq, log_l, Ma, Mf, Md]
    alpha = results[0]
    falpha = results[1]

    #------------------------- not-NaNs -------------------------#
    alpha_notnans = ~ np.isnan(alpha)
    falpha_notnans = ~ np.isnan(falpha)
    notnan_indices = alpha_notnans & falpha_notnans
    alpha = alpha[notnan_indices]
    falpha = falpha[notnan_indices]


    #======================= PLOT =======================#
    fig = plt.figure(constrained_layout=True, figsize=(14, 8))
    plt.style.use('classic')
    fig.set_facecolor('none')
    linewidths, fontsizes = 2.5, 15
    plt.rc('lines', linewidth=linewidths)
    plt.rc('axes', linewidth=linewidths)
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams.update({'mathtext.default':'regular'})
    gs = fig.add_gridspec(2, 2)

    #--------------------- LEFT PANEL ---------------------#
    ax1 = fig.add_subplot(gs[0:,0])
    ax1.set_title("MULTIFRACTAL SPECTRUM\n" + filename, fontsize=fontsizes+5, pad=15)
    ax1.plot(results[0], results[1], linestyle='-', marker='.', markersize=10, color='k')
    ax1.tick_params(axis="both", direction="in", left=True, width=linewidths, length=4, labelsize=fontsizes)
    ax1.set_xlabel(r"$Hölder \ exponent \ \alpha$", fontsize=fontsizes+5)
    ax1.set_ylabel(r"$Hausdorff \ dimension \ f(\alpha)$", fontsize=fontsizes+5)
    #ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    #ax1.set_xlabel(r"$\alpha$", fontsize=fontsizes)
    amin_index = np.where(results[0]==min(results[0]))[0]
    amax_index = np.where(results[0]==max(results[0]))[0]
    ax1.text(0.5, 0.50, r"$\Delta\alpha=%.3f$" % (max(results[0]) - min(results[0])), color='k', fontsize=fontsizes, ha='center', va='center', transform=ax1.transAxes)
    ax1.text(0.5, 0.450, r"$f(\alpha_{max})-f(\alpha_{min})=%.3f$" % abs(results[1][amax_index] - results[1][amin_index]), color='k', fontsize=fontsizes, ha='center', va='center', transform=ax1.transAxes)
    #ax1.text(0.1, 0.80, "$m_1=7$ \n$m_2=8$ \n \n$p=4$ \n$p_c=4$", fontsize=fontsizes, ha='center', va='center', transform=ax.transAxes) 
    ax1.axis([min(results[0]) - 0.1, max(results[0]) + 0.1, min(results[1]) - 0.1, max(results[1]) + 0.1])

    #------------------- UPPER LEFT PANEL -------------------#
    ax2 = fig.add_subplot(gs[0,1])
    ax2.set_title("$Scaling \ of \ the \ partition \ function \ Z(l)$", fontsize=fontsizes+5, pad=15)
    ax2.set_xlabel("$log \ of \ the \ lentgh \ scales, \ log_{10}(l)$", fontsize=fontsizes+5)
    ax2.set_ylabel("$log \ of \ the \ q-th \ moment, \ log_{10}(Z_q(l))$", fontsize=fontsizes+5)
    ax2.set_xlim([min(results[-4]) - .3, max(results[-4]) + .3])
    ax2.set_ylim([int(min(results[-1][-1])) - 10, int(max(results[-1][0])) + 10])
    color_palette = plt.cm.get_cmap('viridis', len(results[-1]))
    for i in range(0, len(results[-1]), int(q_range[1]/5)):
        ax2.plot(results[-4], results[-1][i], marker='o', ms=10, ls='-', color=color_palette(i), label=f"$q={q_values[i]}$")
    ax2.legend(ncol=1, prop={'size':12}, bbox_to_anchor=(1.23, 1.05), numpoints=1,
               labelspacing=0.4, handlelength=2, handletextpad=0.8, framealpha=0)

    #------------------- DOWN RIGHT PANEL -------------------#
    ax3 = fig.add_subplot(gs[1,1])
    ax3.set_title("$Generalized \ fractal \ dimension \ spectrum$", fontsize=fontsizes+5, pad=15)
    ax3.plot(q_values, results[2], marker='o', ms=10, ls='', color='k')
    #ax3.axis([q_range[0]-1, q_range[-1]+1, Dq[0]-1, Dq[-1]+1])
    ax3.set_xlabel("$Moment \ order \ q$", fontsize=fontsizes+5)
    ax3.set_ylabel("$Fractal \ dimension \ D(q)$", fontsize=fontsizes+5)

    plt.show()

def mfs_width(data, length = 2 ** 7, q_range = (-40, 40)):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(length - 1, N):

        x = data[t - (length - 1):t + 1].values

        l = floor(numpy.log2(len(x)))
        scale_range = (1, l)
        q_values = numpy.arange(q_range[0], q_range[1] + 1)
        scale_values = numpy.arange(scale_range[0], scale_range[1] + 1)

        results = chhabra_jensen_analysis(x, q_values, scale_values)
        delta_alpha = max(results[0]) - min(results[0])
        df.loc[df.index[t]] = [*delta_alpha]

        print("t = %d; Multifractal spectrum width = %f" % (t, delta_alpha), end='')
        print("\t\t\t", end='\r')

    return None

def mfs_height(data, length = 2 ** 7, q_range = (-40, 40)):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(length - 1, N):

        x = data[t - (length - 1):t + 1].values

        l = floor(numpy.log2(len(x)))
        scale_range = (1, l)
        q_values = numpy.arange(q_range[0], q_range[1] + 1)
        scale_values = numpy.arange(scale_range[0], scale_range[1] + 1)

        results = chhabra_jensen_analysis(x, q_values, scale_values)
        amin_index = np.where(results[0]==min(results[0]))[0]
        amax_index = np.where(results[0]==max(results[0]))[0]
        delta_falpha = abs(results[1][amax_index] - results[1][amin_index])
        df.loc[df.index[t]] = [*delta_falpha]

        print("t = %d; Multifractal spectrum height = %f" % (t, delta_falpha), end='')
        print("\t\t\t", end='\r')


