
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
def _mergeSort(arr: list, tmp: list, l, r):
    if l == r - 1: 
        return
    m = (l+r+1) // 2
    _mergeSort(arr, tmp, l, m)
    _mergeSort(arr, tmp, m, r)
    merge(arr, tmp, l, m, r)

def mergeSort(arr: list):
    tmp = [0] * len(arr)
    _mergeSort(arr, tmp, 0, len(arr))



def solve(problem: Problem):
    pointlist = problem.pointlist
    itp = problem.itp

    pointlist.sort(key=lambda p: p.x)
    u = 0
    v = 0
    ans = -1

    def _solve(l, r):
        if l >= r - 1:
            return -1
        
        m = (l + r + 1) / 2
        


def generateProblem(w, h, n) -> Problem:
    problem = Problem()
    for _ in range(n):
        x = random.random() * w
        y = random.random() * h

        problem.addPoint(x, y)
    return problem

problem = generateProblem(10, 10, 4)
solve(problem)