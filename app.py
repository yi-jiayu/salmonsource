from itertools import takewhile

import requests
from flask import Flask, redirect, render_template, request, url_for

from config import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret_key


def get_coop_results(splatnet_cookie):
    if app.debug:
        import json

        with open("coop.json") as f:
            return json.load(f)["results"]
    res = requests.get(
        "https://app.splatoon2.nintendo.net/api/coop_results",
        cookies={"iksm_session": splatnet_cookie},
    )
    return res.json()["results"]


@app.route("/")
def home():
    splatnet_cookie = request.args.get("splatnet_cookie")
    if not splatnet_cookie:
        return redirect(url_for("signin"))
    else:
        refresh = request.args.get("refresh")
        shifts = get_coop_results(splatnet_cookie)
        latest_rotation_start_time = shifts[0]["schedule"]["start_time"]
        latest_rotation_shifts = takewhile(
            lambda shift: shift["schedule"]["start_time"] == latest_rotation_start_time,
            shifts,
        )
        grade_points = [shift["grade_point"] for shift in latest_rotation_shifts]
        grade_points.reverse()
        x = list(range(len(grade_points)))
        return render_template("home.html", x=x, y=grade_points, refresh=refresh)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        splatnet_cookie = request.form["splatnet_cookie"]
        return redirect(url_for("home", splatnet_cookie=splatnet_cookie))
    else:
        return render_template("signin.html")
