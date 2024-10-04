import numpy
import pandas
from lib.calculations.salib import Complexity

def complexity(data: pandas.Series, period: int):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values
        binary_sequence = Complexity.binarizer(x)
        complexity = Complexity.lempel_ziv(numpy.array(binary_sequence))
        df.loc[df.index[t]] = [complexity]

        print("t = %d; Lempel-Ziv complexity = %f" % (t, complexity), end='')
        print("\t\t\t", end='\r')

    return df