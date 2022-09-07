from flask import Flask, render_template
from streamlit import form

app = Flask(__name__)


@app.route("/")
def home():  # put application's code here
    return render_template("home.html")

@app.route("/seats")
def seats():
    return render_template("seats.html")

if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)
