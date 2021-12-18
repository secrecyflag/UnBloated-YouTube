from . import app
from flask import render_template, url_for, request, redirect
from frontend_constants import Titles, Methods
from api import search


@app.route("/", methods=[Methods.POST, Methods.GET])
@app.route("/index", methods=[Methods.POST, Methods.GET])
def index():
    return render_template("index.html", title=Titles.INDEX)


@app.route("/results", methods=[Methods.POST])
def results():
    query = ""
    if request.method == Methods.POST:
        query = request.form["query"]
    return render_template("results.html", title=Titles.RESULTS, query=query, suggestions=search.search_suggestions(query))
