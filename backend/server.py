from os import abort
from flask import Flask, redirect, request
from algorithm import Problem, generateProblem
from benchmark import buildTestSet, readableTestResult, test

app = Flask(__name__, static_folder="../dist/", static_url_path='/')

@app.route("/")
def index():
    return redirect("/index.html")

@app.route("/api/hello")
def hello():
    return {"data": "hello world!"}


@app.route("/api/solve", methods=["POST"])
def solve():
    data = request.json["data"]
    testSet = buildTestSet(len(data))
    problem = Problem()
    for e in data:
        problem.addPoint(e["x"], e["y"])
    
    result = test(testSet, problem)
    
    return readableTestResult(result, problem)


@app.route("/api/genandsolve")
def genAndSolve():
    n = request.args.get("n", -1, int)
    if n < 2:
        abort(400)
    testSet = buildTestSet(n)
    problem = generateProblem(100, 100, n)
    result = test(testSet, problem)
    return readableTestResult(result, problem)



app.run(port=8089)