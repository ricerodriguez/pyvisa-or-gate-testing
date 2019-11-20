import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics as s
    #give us a test type and a list
def Histogram(test,results,mean, stdev):
    testRes = pd.Series(results)
    testRes.plot.hist(grid = True, bins = 20, rwidth = 0.9, color = '#60ac8c')

    plt.title ('Results of {} Test'.format(test))
    plt.ylabel('Frequency')
    plt.xlabel('Voltage ')
    plt.grid(axis = 'y', alpha = .75)

    plt.savefig('{}_Histogram'.format(test))
    plt.show()


if __name__ == '__main__':
    results = [.2,.56,.8,.4,.5,.1,.6,.7,.6,.8,.4,1,.58,.5,.8]
    test = 'Example'
    mean = round(s.mean(results),3)
    stdev = round(s.stdev(results),3)

    Histogram(test,results,mean,stdev)
