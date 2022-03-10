import datetime
import functools
from pprint import pprint

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
            "bubble": withArgs(A.bubbleSort),
            "builtin": withArgs(A.builtinSort)
        }
    }

    if n <= 1000:
        testSet["func"]["brute"] = timerBrute
    
    return testSet


def test(testSet, problem):
    result = {}
    for fn in testSet["func"]:
        oriList = problem.pointlist[:]
        result[fn] = testSet["func"][fn](problem)
        problem.poinlist = oriList
    return result


def toPos(problem: A.Problem, id):
    return {
        "x": problem.itp[id].x,
        "y": problem.itp[id].y,
    }


def readableTestResult(result, problem):
    rtn = {}
    for k in result:
        rtn[k] = {
            "time": result[k][0],
            "point": {"u": toPos(problem, result[k][1][1]), "v": toPos(problem, result[k][1][2])},
            "dis": result[k][1][0]
        }
    return rtn


def quickTest(n):
    pro = A.generateProblem(10, 10, n)
    s = buildTestSet(n)
    pprint(test(s, pro))


def multipleTest(repeat = 5):
    data = []
    ks = set()

    for i in range(2, 21):
        print(f"test: {i}, n = {2**i}")
        n = 2**i
        problem = A.generateProblem(100, 100, n)
        tSet = buildTestSet(n)

        aveRst = {}

        for _ in range(repeat):
            r = test(tSet, problem)
            result = readableTestResult(r, problem)
            for k in result:
                aveRst[k] = (aveRst.get(k) or 0) + result[k]["time"]

        for k in aveRst: aveRst[k] /= repeat
        data.append(aveRst)
        ks |= aveRst.keys()

    with open("data.csv", "w") as file:
        for k in ks:
            file.write(f"{k}, ")
        file.write("\n")

        for e in data:
            for k in ks:
                file.write(f"{e.get(k) or 0}, ")
            file.write("\n")
