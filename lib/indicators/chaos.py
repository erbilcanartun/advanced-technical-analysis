import numpy
import pandas
from lib.salib import Chaos

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
        lyapunov = Chaos.lyapunov_exponent(x, candle_range=period, initial_diameter=diameter, display=False)
        df.loc[df.index[t]] = [lyapunov]

        print("t = %d; Lyapunov exp. = %f" % (t, lyapunov), end='')
        print("\t\t\t", end='\r')

    return df