import pandas
from lib.salib import Entropy

def shen(data: pandas.Series, period: int):

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

def apen(data: pandas.Series, period: int):

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