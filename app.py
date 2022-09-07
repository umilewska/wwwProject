from flask import Flask, render_template, redirect, url_for, request
import sqlalchemy
from streamlit import form

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form.get('action_movie') == 'batman':
            return redirect(url_for("seanseBatman"))
        elif request.form.get('action_movie') == 'django':
            return redirect(url_for("seanseDjango"))
        elif request.form.get('action_movie') == 'bullet':
            return redirect(url_for("seanseBulletTrain"))
    else:
        return render_template("home.html")

@app.route("/seanseBatman", methods=["POST", "GET"])
def seanseBatman():
    return render_template("seanceBatman.html")

@app.route("/seanseDjango", methods=["POST", "GET"])
def seanseDjango():
    return render_template("seanceDjango.html")

@app.route("/seanseBulletTrain", methods=["POST", "GET"])
def seanseBulletTrain():
    return render_template("seanceBulletTrain.html")

# ------------------------ seats -----------------------------

@app.route("/seanseBatman/seats", methods=["POST", "GET"])
def seatsBatman():
    return render_template("seats.html")

@app.route("/seanseDjango/seats", methods=["POST", "GET"])
def seatsDjango():
    return render_template("seats.html")

@app.route("/seanseBulletTrain/seats", methods=["POST", "GET"])
def seatsBulletTrain():
    return render_template("seats.html")


if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)
