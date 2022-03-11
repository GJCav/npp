
from cmath import sqrt
from typing import Dict
import random


class Point:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.id = 0


def distanceSq(p1, p2):
    return (p1.x-p2.x) ** 2 + (p1.y - p2.y) ** 2

def distance(p1, p2):
    return distanceSq(p1, p2)

class Problem:
    def __init__(self) -> None:
        self.itp: Dict[int, Point] = {}
        self.pointlist = []

    def addPoint(self, x, y):
        p = Point()
        p.x = x
        p.y = y
        p.id = len(self.itp)

        self.itp[p.id] = p
        self.pointlist.append(p)


def merge(arr: list, tmp: list, l: int, m: int, r: int, le = lambda x, y: x <= y):
    """
    merge [l, m-1] and [m, r-1]
    """
    i = l
    j = m
    for k in range(l, r):
        if i == m:
            tmp[k] = arr[j]
            j += 1
        elif j == r:
            tmp[k] = arr[i]
            i += 1
        elif le(arr[i], arr[j]):
            tmp[k] = arr[i]
            i += 1
        else:
            tmp[k] = arr[j]
            j += 1
    
    for k in range(l, r):
        arr[k] = tmp[k]


## 用于确认merge的正确性
def _mergeSort(arr: list, tmp: list, l, r, key = lambda x: x):
    if l >= r - 1: 
        return
    m = (l+r+1) // 2
    _mergeSort(arr, tmp, l, m, key)
    _mergeSort(arr, tmp, m, r, key)
    merge(arr, tmp, l, m, r, lambda x, y: key(x) <= key(y))

def mergeSort(arr: list, key = lambda x: x):
    tmp = [0] * len(arr)
    _mergeSort(arr, tmp, 0, len(arr), key)

def swap(arr, i, j):
    x = arr[i]
    arr[i] = arr[j]
    arr[j] = x

def insertSort(arr: list, l, r, key):
    for i in range(l+1, r):
        k = arr[i]
        j = i-1
        while j >= l and key(arr[j]) > key(k):
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = k

def selectSort(arr: list, l, r, key):
    for i in range(l, r):
        ith = i
        for j in range(i+1, r):
            if key(arr[j]) < key(arr[ith]):
                ith = j
        swap(arr, i, ith)

def bubbleSort(arr: list, l, r, key):
    flag = True
    while flag:
        flag = False
        for i in range(l, r-1):
            if key(arr[i]) > key(arr[i+1]):
                flag = True
                swap(arr, i, i+1)

def builtinSort(arr: list, l, r, key):
    t = arr[l:r]
    t.sort(key=key)
    arr[l:r] = t

def solveBrute(problem: Problem):
    arr = problem.pointlist
    uid = 0
    vid = 0
    ans = float("inf")
    
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            curDis = distanceSq(arr[i], arr[j])
            if curDis < ans:
                ans = curDis
                uid = arr[i].id
                vid = arr[j].id

    return (sqrt(ans).real, uid, vid)


def solve(problem: Problem, sortFunc = None):
    pointlist = problem.pointlist
    tmpList = [0] * len(pointlist)

    # pointlist.sort(key=lambda p: (p.x, p.y))
    mergeSort(pointlist, lambda p: (p.x, p.y))

    uid = -1
    vid = -1
    ans = float("inf") # 为了加速，这里使用的是距离的平方，这里容易导致实现出错。

    def _solve(l, r):
        nonlocal uid, vid, ans

        if sortFunc and r - l <= 30:
            sortFunc(pointlist, l, r, key = lambda p: p.y)
            for i in range(l, r):
                for j in range(i+1, r):
                    if (pointlist[j].y - pointlist[i].y) ** 2 >= ans:
                        break
                    curDis = distanceSq(pointlist[i], pointlist[j])
                    if curDis < ans:
                        ans = curDis
                        uid = pointlist[i].id
                        vid = pointlist[j].id
            return ans
        elif l >= r - 1:
            return float("inf")
        
        m = (l + r + 1) // 2
        midx = pointlist[m].x

        leftans = _solve(l, m)
        rightans = _solve(m, r)
        merge(pointlist, tmpList, l, m, r, lambda a, b: a.y <= b.y)
        
        subAns = min(leftans, rightans)

        for i in range(l, r):
            if abs(pointlist[i].x - midx) ** 2 >= subAns: continue
            for j in range(i+1, r):
                if (pointlist[j].y - pointlist[i].y) ** 2 >= subAns:
                    break
                curDis = distanceSq(pointlist[i], pointlist[j])
                if curDis < ans:
                    ans = curDis
                    uid = pointlist[i].id
                    vid = pointlist[j].id
        
        return ans

    _solve(0, len(pointlist))

    return (sqrt(ans).real, uid, vid)


def generateProblem(w, h, n) -> Problem:
    problem = Problem()
    for _ in range(n):
        x = random.random() * w
        y = random.random() * h

        problem.addPoint(x, y)
    return problem


def checkCorrectness():
    sortFuncs = [
        insertSort,
        selectSort,
        bubbleSort
    ]

    fail = False
    for _ in range(100):
        print(f"turn {_}")
        problem = generateProblem(10, 10, 5000)
        __l = [(p.x, p.y) for p in problem.pointlist]
        resA = solve(problem)
        resB = solveBrute(problem)

        pa = set([resA[1], resA[2]])
        pb = set([resB[1], resB[2]])
        if pa != pb:
            fail = True
            print("Fail at B")
            print(__l)
            break

        for f in sortFuncs:
            random.shuffle(problem.pointlist)
            __l = [(p.x, p.y) for p in problem.pointlist]
            resC = solve(problem, sortFunc=f)
            pc = set([resC[1], resC[2]])
            if pa != pc:
                fail = True
                print("Fail at C, " + f.__name__)
                # print(__l)
                break

        if fail:
            break