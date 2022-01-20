from . import app, SETTINGS_OBJ 
from flask import render_template, url_for, request, redirect
from frontend_constants import Titles, Methods
from api import search, fetch_video


@app.route("/", methods=[Methods.POST, Methods.GET])
@app.route("/index", methods=[Methods.POST, Methods.GET])
def index():
    return render_template("index.html", title=Titles.BLANK)


@app.route("/results", methods=[Methods.POST])
def results():
    query = ""
    if request.method == Methods.POST:
        query = request.form["query"]
    return render_template("results.html", title=Titles.RESULTS, query=query, results=search.search_results)


@app.route("/watch", methods=[Methods.GET, Methods.POST])
def watch():
    if request.method == Methods.POST:
        quality = request.form["quality_select"]
    else:
        quality = SETTINGS_OBJ.get_default_quality()
    video_id = request.args["v"]
    url = "https://www.youtube.com/watch?v=" + video_id
    urls, qualities = fetch_video.fetch_video(url, quality=quality)
    video_title = fetch_video.get_video_title(url=url)
    return render_template("watch.html", video_id=video_id, title=Titles.BLANK, urls=urls, video_title=video_title, qualities=qualities)


@app.route("/settings", methods=[Methods.GET, Methods.POST])
def settings():
    if request.method == Methods.POST:
        SETTINGS_OBJ.write_settings(request.form.to_dict(flat=False)) 
    return render_template("settings.html", title=Titles.SETTINGS)

