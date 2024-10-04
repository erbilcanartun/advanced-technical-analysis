import pandas
from scipy.spatial.distance import pdist, squareform

from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation, RPComputation
from pyrqa.image_generator import ImageGenerator


def rate(data: pandas.Series, period: int):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values

        # RQA Analysis
        reconstructed = TimeSeries(x, embedding_dimension=2, time_delay=2)
        settings = Settings(reconstructed, analysis_type=Classic,
                            neighbourhood=FixedRadius(0.65),
                            similarity_measure=EuclideanMetric, theiler_corrector=1)
        computation = RQAComputation.create(settings, verbose=False)
        result = computation.run()
        RR = result.recurrence_rate
        df.loc[df.index[t]] = [RR]

        print("t = %d; RR = %f" % (t, RR), end='')
        print("\t\t\t", end='\r')

    return df

def determinism(data: pandas.Series, period: int):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values

        # RQA Analysis
        reconstructed = TimeSeries(x, embedding_dimension=2, time_delay=2)
        settings = Settings(reconstructed,
                            analysis_type=Classic,
                            neighbourhood=FixedRadius(0.65),
                            similarity_measure=EuclideanMetric,
                            theiler_corrector=1)
        computation = RQAComputation.create(settings, verbose=False)
        result = computation.run()
        DET = result.determinism
        df.loc[df.index[t]] = [DET]

        print("t = %d; DET = %f" % (t, DET), end='')
        print("\t\t\t", end='\r')
    return df

def laminarity(data: pandas.Series, period: int):

    N = len(data)
    df = pandas.DataFrame(index=data.index, columns=["indicator"])
    print(f"Period = {period}\nData length = {N}\n")

    for t in range(period - 1, N):

        x = data[t - (period - 1):t + 1].values

        # RQA Analysis
        reconstructed = TimeSeries(x, embedding_dimension=2, time_delay=2)
        settings = Settings(reconstructed,
                            analysis_type=Classic,
                            neighbourhood=FixedRadius(0.65),
                            similarity_measure=EuclideanMetric,
                            theiler_corrector=1)
        computation = RQAComputation.create(settings, verbose=False)
        result = computation.run()
        LAM = result.laminarity

        df.loc[df.index[t]] = [LAM]

        print("t = %d; LAM = %f" % (t, LAM), end='')
        print("\t\t\t", end='\r')
        return df

def recurrence_plot(series, eps=0.10, steps=10):

    d = pdist(series[:, None])
    d = numpy.floor(d / eps)
    d[d>steps] = steps
    Z = squareform(d)
    return Z
