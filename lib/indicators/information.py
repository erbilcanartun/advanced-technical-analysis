import numpy
import pandas
from pyinform import mutual_info
from lib.salib import Information


def mutual(data: pandas.Series, period: int, delay: int,
          max_delay: int, method: str = 'constant delay'):
    # Delay time (should be less than 'length')

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])

    if method == 'constant delay':

        print(f"Period = {period}\nData length = {N}\n")
        for t in range(period - 1 + delay, N):

            unlagged = data[t - (period - 1) - delay:t + 1 - delay].values
            lagged = data[t - (period - 1):t + 1].values

            info = Information.mutual(unlagged, lagged, local=False)
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
        raise ValueError("Choose method.")

    return df