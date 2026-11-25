"""
Optimize Python Code with timeit / Using the timeit Module
    * What is the performance of this recursive implementation of Longest Increasing Subsequence?
"""

import random
from timeit import timeit


def shuffled(A):
    random.shuffle(A)
    return A


def timing_lis_rec_trial():
    T = 100
    for N in range(30, 66, 5):
        result = timeit(f"list_rec(shuffled(R))", setup=f"R=list(range({N}))")
    result /= T
    print("list rec", N, result)

