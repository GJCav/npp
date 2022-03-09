import datetime
import functools
from imghdr import tests
from pprint import pprint
import json
from random import shuffle
from unittest import result

import algorithm as A

def timeit(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        st = datetime.datetime.now()
        r = func(*args, **kwargs)
        ed = datetime.datetime.now()
        return (ed - st).total_seconds(), r
    return inner


def buildTestSet(n):
    timerSolve = timeit(A.solve)
    timerBrute = timeit(A.solveBrute)

    def withArgs(sf):
        def inner(*args, **kwargs):
            return timerSolve(sortFunc = sf, *args, **kwargs)
        return inner

    testSet = {
        "n": n,
        "func": {
            "solve": timerSolve,
            "select": withArgs(A.selectSort),
            "insert": withArgs(A.insertSort),
            "bubble": withArgs(A.bubbleSort)
        }
    }

    if n <= 1000:
        testSet["func"]["brute"] = timerBrute


def test(testSet):
    problem = A.generateProblem(100, 100, testSet["n"])
    result = {}
    for fn in testSet["func"]:
        result[fn] = testSet["func"][fn](problem)
    return result