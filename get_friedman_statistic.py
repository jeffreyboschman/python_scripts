import os
import sys
import numpy as np
import pandas as pd
import argparse
import scipy.stats
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

def main(input_file, alpha, delimiter, skiprows):
    df = pd.read_table(input_file, delimiter=delimiter, skiprows=skiprows)
    print(f'\nAs a sanity check, here is the DataFrame object used. The rows should be the different treatment conditions compared (k), and the columns should be the different measurements (n).\n')
    print(df)
    
    methods = df.index.values
    array = df.to_numpy(copy=True)
    avg_ranks = get_average_ranks(*array)
    print_average_ranks(methods, avg_ranks)
    stat, pvalue = scipy.stats.friedmanchisquare(*array)
    print(f'The calculated Friedman statistic is {stat}\n')

    if pvalue <= alpha:
        print(f'The p-value of {pvalue} is less than or equal to the significance level {alpha}, which indicates statistical significance and thus we reject the null hypothesis that all methods are treatment conditions are equal. i.e. the results are statistically different\n')
    else:
        print(f'The p-value is {pvalue} is greater than the significance level {alpha}, which indicates statistical non-significance and thus we fail to reject the null hypothesis that all methods are treatment conditions are equal. i.e. the results are not statistically different.\n')

    k = len(array)
    n = len(array[0]) 
    if n<=13 and k<=5:
        print(f'However, this p-value assumes a chi-squared distribution which is only reliable for a large number of observations (n>13) or a large number of compared treatment conditions (k>5). We used {n} observations for {k} treatment conditions, so for a more accurate p-value please compare the calculated Friedman statistic with a table specifically prepared for the Friedman test. ex. https://psych.unl.edu/psycrs/handcomp/hcfried.PDF')

def get_average_ranks(*args):
    '''modified from https://github.com/scipy/scipy/blob/v1.6.0/scipy/stats/stats.py#L7374-L7436'''
    k = len(args)
    n = len(args[0])
    data = np.vstack(args).T
    data = data.astype(float)
    ranks = np.zeros([n,k])
    for i in range(n):
        ranks[i] = scipy.stats.rankdata(data[i])
    reverse_ranks = abs(ranks - (k+1))
    return np.average(reverse_ranks, axis=0) 

def print_average_ranks(methods_list, avg_ranks_list):
    output = '\n||Method||Avg Rank||\n'
    for idx, method in enumerate(methods_list):
        output += f'|{method}|{avg_ranks_list[idx]:.2f}|\n' 
    print(output)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description =''' Calculates the friedman statistic. Ideally, there should be at least 3 treatment conditions compared (k>=3) and at least 10 different measurements for each (n>=10)''')

    parser.add_argument('--input_file', type=str, help='The full path to a textfile that contains the results of different methods and their set of measurements')
    parser.add_argument('--alpha', type=float, default=0.05, help='The significance level')
    parser.add_argument('--delimiter', type=str, default="\s+", help='The delimiter for the results in your textfile. Common inputs are ",", "|", or "\s+" (for multiple spaces)')
    parser.add_argument('--skiprows', type=int, default=1, help='How many rows to skip for reading the textfile into a dataframe object')

    args = parser.parse_args()

    main(args.input_file, args.alpha, args.delimiter, args.skiprows)
