import paypalrestsdk
from flask import Flask, render_template, redirect, url_for, request, jsonify
import sqlalchemy
from streamlit import form

app = Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AS8Ip1U8_Eh_9iHTvtCIBg3O8QhwbMeWlLuQg1vpfa08aNALHOV4JaMvs18wGIYmMXFOB2ROEGHJgdFo",
  "client_secret": "EK0L-coYgnXh54r44rydlEIBFDjkeom1SJeS3hPgsoN_9LXuUCFOEMcCOmIiDUrS3QVIoURrdCdWYPxW" })


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

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "bilet ulgowy",
                    "sku": "12345",
                    "price": "12.50",
                    "currency": "PLN",
                    "quantity": 1},
                {
                    "name": "bilet normanly",
                    "sku": "12345",
                    "price": "17.50",
                    "currency": "PLN",
                    "quantity": 1}],
            },
            "amount": {
                "total": "30.00",
                "currency": "PLN"},
            "description": "Zakup biletu do kina."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)
