import numpy
import pandas
from utils.salib import *

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
        complexity = Complexity..lempel_ziv_complexity(np.array(binary_sequence))
        df.loc[df.index[t]] = [complexity]

        print("t = %d; Lempel-Ziv complexity = %f" % (t, complexity), end='')
        print("\t\t\t", end='\r')

    return df





