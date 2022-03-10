from os import abort
from flask import Flask, request
from algorithm import Problem, generateProblem
from benchmark import buildTestSet, readableTestResult, test

app = Flask("npp")

@app.route("/hello")
def hello():
    return {"data": "hello world!"}


@app.route("/solve", methods=["POST"])
def solve():
    data = request.json["data"]
    testSet = buildTestSet(len(data))
    problem = Problem()
    for e in data:
        problem.addPoint(e["x"], e["y"])
    
    result = test(testSet, problem)
    
    return readableTestResult(result, problem)


@app.route("/genandsolve")
def genAndSolve():
    n = request.args.get("n", -1, int)
    if n < 2:
        abort(400)
    testSet = buildTestSet(n)
    problem = generateProblem(100, 100, n)
    result = test(testSet, problem)
    return readableTestResult(result, problem)

app.run(port=8089)