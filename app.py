import stripe as stripe
from flask import Flask, render_template, redirect, url_for, request, abort
import sqlalchemy
from streamlit import form

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51LfnIsEppafJpnA12mXgW9hAjYCeZdhwmgUMHtHaSROmeOoiAUDSzu52Es5VLowz70WZLcm49jWExfn34GEuvl690064rVJpQa'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51LfnIsEppafJpnA1yhI6Es3uPRQgb4Vl1YcnTLjObPt3cAnU35oDKh08unvdR09YpdiWQJkzGkyk5pKPS6XvlHlP00c8TRbQdf'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

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

@app.route("/payment")
def payment():
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1LfndoEppafJpnA1v2Tm3qcL',
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment', _external=True),
        )
        return render_template(
            'home.html',
            checkout_session_id = session['id'],
            checkout_public_key = app.config['STRIPE_PUBLIC_KEY']
            )


if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)
