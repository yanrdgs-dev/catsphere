from bottle import Bottle, route, run, request, static_file, redirect, template, response
from app.controllers.application import Application

app = Bottle()
ctl = Application()

@app.route("/static/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root="./app/static")

@app.route("/")
def index(info=None):
    return ctl.render("index")

if __name__ == "__main__":
    run(app, host="0.0.0.0", port="8080", debug=True)