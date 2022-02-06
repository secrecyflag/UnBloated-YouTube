from . import app, SETTINGS_OBJ 
from flask import render_template, url_for, request, redirect
from frontend_constants import Titles, Methods
from api import search, fetch_video


def is_dark_mode():
    return True if SETTINGS_OBJ.get_dark_mode() == "1" else False


def is_hdr():
    return True if SETTINGS_OBJ.get_hdr() == "1" else False


@app.route("/", methods=[Methods.POST, Methods.GET])
@app.route("/index", methods=[Methods.POST, Methods.GET])
def index():
    return render_template("index.html", title=Titles.BLANK, dark_mode=is_dark_mode())


@app.route("/results", methods=[Methods.POST])
def results():
    query = ""
    if request.method == Methods.POST:
        query = request.form["query"]
    return render_template("results.html", title=Titles.RESULTS,
                            query=query, 
                            results=search.search_results, dark_mode=is_dark_mode())


@app.route("/watch", methods=[Methods.GET, Methods.POST])
def watch():
    if request.method == Methods.POST:
        quality = request.form["quality_select"]
    else:
        quality = SETTINGS_OBJ.get_default_quality()
    video_id = request.args["v"]
    url = "https://www.youtube.com/watch?v=" + video_id
    urls, qualities = fetch_video.fetch_video(url, quality=quality, 
                                              hdr=True if SETTINGS_OBJ.get_hdr() == "1" else False)
    video_src = fetch_video.get_video_src()
    video_info = fetch_video.get_video_info(url=url, html=video_src)
    recommendations = fetch_video.get_recommendations()
    return render_template("watch.html", video_id=video_id, title=Titles.BLANK,
                            urls=urls, video_info=video_info,
                            qualities=qualities, dark_mode=is_dark_mode(),
                            recommendations=recommendations)


@app.route("/settings", methods=[Methods.GET, Methods.POST])
def settings():
    if request.method == Methods.POST:
        form_dict = request.form.to_dict(flat=False)
        form_dict["darkMode"] = form_dict["darkMode"][-1]
        form_dict["HDR"] = form_dict["HDR"][-1]
        SETTINGS_OBJ.write_settings(form_dict) 
    return render_template("settings.html", title=Titles.SETTINGS, dark_mode=is_dark_mode(), hdr=is_hdr())

