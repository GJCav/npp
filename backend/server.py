from flask import Flask, request
from algorithm import Problem
from benchmark import buildTestSet, test

app = Flask("npp")

@app.route("/hello")
def hello():
    return {"data": "hello world!"}


def toPos(problem: Problem, id):
    return {
        "x": problem.itp[id].x,
        "y": problem.itp[id].y,
    }


@app.route("/solve", methods=["POST"])
def solve():
    data = request.json["data"]
    testSet = buildTestSet(len(data))
    problem = Problem()
    for e in data:
        problem.addPoint(e["x"], e["y"])
    
    result = test(testSet, problem)
    
    rtn = {}
    for k in result:
        rtn[k] = {
            "time": result[k][0],
            "point": {"u": toPos(problem, result[k][1][1]), "v": toPos(problem, result[k][1][2])},
            "dis": result[k][1][0].real
        }
    return rtn

app.run(port=8089)