from flask import Flask

app = Flask("npp")

@app.route("/hello")
def hello():
    return {"data": "hello world!"}

app.run(port=8089)