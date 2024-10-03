import numpy
from scipy import stats
from pyinform import mutual_info
import matplotlib.pyplot


class Chaos:

    def lyapunov_exponent(time_series, candle_range=100, initial_diameter=0.001, display=False):

        time_series, N = numpy.array(time_series), candle_range
        #time_series = (time_series - np.mean(time_series)) / np.std(time_series) # standardization

        exponents = [[] for i in range(N)]

        for i in range(N):
            for j in range(i + 1, N):

                if numpy.abs(time_series[i] - time_series[j]) < initial_diameter:

                    for k in range(min(N - i, N - j)):

                        d = numpy.abs(time_series[i+k] - time_series[j+k])

                        if d == 0. or numpy.isnan(d): continue # Avoid zero differences
                        else: pass

                        exponents[k].append(numpy.log(d))

        lyapunovs = []
        for i in range(len(exponents)):
            if len(exponents[i]):
                lyapunovs.append([i, numpy.mean(exponents[i])])


        # Linear regression

        x = numpy.array(lyapunovs)[:,0]
        y = numpy.array(lyapunovs)[:,1]

        results = []
        cut = 2 # We need to start from 3 to avoid R^2=1 at the beginning
        for i in range(x.size):

            cut += 1

            X = x[:cut]
            Y = y[:cut]

            slope, intercept, r, p, se = stats.linregress(X, Y)
            results.append((slope, intercept, cut, r**2))

        results_T = list(zip(*results))
        r_sqr = max(results_T[3])
        i = results_T[3].index(r_sqr)
        lyapunov_exp = results[i][0] # Slope is the Lyapunov exponent
        intercept = results[i][1]
        cut = results[i][2]
        X = X[:cut]

        if display:
            print("Linear regime: [0, %d], R-square = %.3f\n\nLyapunov exponent = %.3f\n" % (cut, r_sqr, lyapunov_exp))

            # Plot
            fig, ax = matplotlib.pyplot.subplots(figsize=(6, 4), dpi=100)

            matplotlib.pyplot.style.use('classic')
            fig.set_facecolor('white')
            linewidths, fontsizes = 2.5, 20

            matplotlib.pyplot.rc('lines', linewidth=linewidths)
            matplotlib.pyplot.rc('axes', linewidth=linewidths)
            matplotlib.pyplot.rcParams['font.family'] = 'Arial'
            matplotlib.pyplot.rcParams.update({'mathtext.default':'regular'})

            ax.plot(x, y, ls=':', marker='.', ms=10, color='red', label="divergence exponents")
            ax.plot(X, lyapunov_exp*X + intercept, ls='-', lw=linewidths, marker='', color='g',
                    ms=10, label="linear fit ($R^2=%.2f$)"%r_sqr)

            ax.tick_params(axis="both", direction="in", left=True,
                           width=linewidths, length=4, labelsize=fontsizes)
            ax.set_xlabel(r"$k$", fontsize=fontsizes)
            ax.set_ylabel(r"$<ln(d(k))>$", fontsize=fontsizes)
            ax.legend(loc='best', ncol=1, prop={'size':12}, numpoints=1,
                      labelspacing=0.5, handlelength=1.4, handletextpad=0.5)

            ax.text(0.5, 0.2, r"$\lambda=%.3f$" % lyapunov_exp, color='k',
                    fontsize=fontsizes-5, ha='center', va='center', transform=ax.transAxes)
            matplotlib.pyplot.show()

        return lyapunov_exp


class Entropy:

    def shannon(series):

        pk = series / numpy.sum(series)
        return -numpy.sum(pk * numpy.log2(pk))


    def approximate(U, m, r):

        N = len(U)

        def _maxdist(x_i, x_j):
            return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

        def _phi(m):
            x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
            C = [len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0) for x_i in x]
            return (N - m + 1.0)**(-1) * sum(numpy.log(C))

        return _phi(m) - _phi(m + 1)


class Information:

    def mutual():
        return mutual_info()



class Complexity:

    def binarizer(array):

        mean = array.mean()

        return [1 if element >= mean else 0 for element in array]


    def lempel_ziv(sequence):
        """
        Calculate Lempel-Ziv's algorithmic complexity using the LZ76 algorithm
        and the sliding-window implementation.

        Reference:

        F. Kaspar, H. G. Schuster, "Easily-calculable measure for the
        complexity of spatiotemporal patterns", Physical Review A, Volume 36,
        Number 2 (1987).

        Input:
          sequence -- array of integers

        Output:
          complexity  -- integer
        """

        sequence = sequence.flatten().tolist()

        i, k, l = 0, 1, 1
        complexity, k_max = 1, 1
        n = len(sequence)

        while True:

            if sequence[i + k - 1] == sequence[l + k - 1]:
                k += 1
                if l + k > n:
                    complexity += 1
                    break
            else:
                if k > k_max:
                    k_max = k
                i += 1
                if i == l:
                    complexity += 1
                    l += k_max
                    if l + 1 > n:
                        break
                    else:
                        i = 0
                        k = 1
                        k_max = 1
                else:
                    k = 1

        return complexity


class Fractal:

    def fractal_analysis(time_series, q_values, scale_values):

        """
        INPUT: time_series, q_values (a range of q values to which the spectrum will be evaluated),
        and scales (window sizes l that vary in a dyadic scale) are all row vectors. This function
        assumes that your time series is all positive values (sign transform it if needed). None
        of the q_values can be between 0 and 1.

        OUTPUT: alpha and falpha scattered against each other give the multifractal spectrum.
        q_values and Dq scattered against each other give the generalised dimensions spectrum.

        Rsqr_alpha, Rsqr_falpha, and Rsqr_Dq are the R-squared values for each of the values in
        alpha, falpha, and Dq respectively.

        mu_scale, Ma, Mf, and Md are the basic matricies from which alpha, falpha, and Dq can be
        constructed by linear regression. They are included in the output mainly for completeness.
        """

        # Initialize
        nq, ns = len(q_values), len(scale_values)
        Ma = numpy.zeros([nq, ns])
        Mf = numpy.zeros([nq, ns])
        Md = numpy.zeros([nq, ns])

        log_l = numpy.log10(2**scale_values) # Window sizes l that vary in a dyadic scale

        alpha = numpy.zeros([nq, 1])
        falpha = numpy.zeros([nq, 1])
        Dq = numpy.zeros([nq, 1])

        Rsquared_alpha = numpy.zeros([nq, 1])
        Rsquared_falpha = numpy.zeros([nq, 1])
        Rsquared_Dq = numpy.zeros([nq, 1])


        # Calculate Ma(ij), Mf(ij), Md(ij)

        for i in range(nq): # Looping through q values

            q = q_values[i]

            for j in range(ns): # Looping through scales

                # Calculate P(l), the cumulative probabilities of the windows
                window = 2**scale_values[j]  # How many windows we will have at this scale
                timeseries_windowed = numpy.reshape(time_series, (-1, window), order="F") # Break the time series into windows
                P = numpy.sum(timeseries_windowed, axis=0) / sum(time_series)


                normalization = sum(P**q)

                # Mα & Mf: A numerical approximation to the equations α(q) and f(q)
                mu = (P**q) / normalization
                Ma[i,j] = sum(mu * numpy.log10(P))
                Mf[i,j] = sum(mu * numpy.log10(mu))


                # Md
                Md[i,j] = numpy.log10(normalization) # Not accounting for q between 0 and 1

                if q > 0 and q <= 1:
                    Md[i,j] = sum(P * numpy.log10(P)) / normalization


            # Regression: α(q) and f(q) can be obtained as the slopes by regressing Mα & Mf against the scales l: Mα ∼ l and Mf ∼ l
            slope_a, intercept, R2_a, p_value, std_err = stats.linregress(-log_l, Ma[i,:])
            slope_f, intercept, R2_f, p_value, std_err = stats.linregress(-log_l, Mf[i,:])
            slope_d, intercept, R2_d, p_value, std_err = stats.linregress(-log_l, Md[i,:])

            alpha[i] = slope_a
            falpha[i] = slope_f

            if q > 0 and q <= 1:
                Dq[i] = slope_d
            else:
                Dq[i] = slope_d / (q - 1)


            Rsquared_alpha[i] = R2_a
            Rsquared_falpha[i] = R2_f
            Rsquared_Dq[i] = R2_d

        return alpha, falpha, Dq, Rsquared_alpha, Rsquared_falpha, Rsquared_Dq, log_l, Ma, Mf, Md