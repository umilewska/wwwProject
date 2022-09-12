import paypalrestsdk
from flask import Flask, render_template, redirect, url_for, request, jsonify
import json
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
        movie_data = request.form.get('movie_button')
        with open('movies.json', 'r', encoding="utf8") as c:
            data = json.load(c)
        movie_name=data[movie_data]['title']
        movie_description=data[movie_data]['description']
        movie_image=data[movie_data]['image']
        movie_hour1 = data[movie_data]['movie_hour1']
        movie_hour2 = data[movie_data]['movie_hour2']
        movie_hour3 = data[movie_data]['movie_hour3']
        c.close()
        reservation = {
            "01": [movie_name]
        }
        with open("reservation.json", "w") as outfile:
            json.dump(reservation, outfile)

        return seanse(movie_image, movie_name, movie_description, movie_hour1, movie_hour2, movie_hour3)
    else:
        return render_template("home.html")


@app.route("/seanse", methods=["POST", "GET"])
def seanse(movie_img, movie_name, movie_desc, movie_hour1, movie_hour2, movie_hour3):
    if request.method == "POST":
        seance_hour = request.form.get('action_seance')
        with open('seats.json', 'r', encoding="utf8") as c:
            data = json.load(c)
        #seance=data[seance_hour]['10:25']
        if request.form.get('action_seance'):
            return seats(movie_name)
        else:
            return render_template("seance.html", movie_img=movie_img, movie_name=movie_name, movie_desc=movie_desc,
                                   movie_hour1=movie_hour1, movie_hour2=movie_hour2, movie_hour3=movie_hour3)
    else:
        return render_template("seance.html", movie_img=movie_img, movie_name=movie_name, movie_desc=movie_desc, movie_hour1=movie_hour1, movie_hour2=movie_hour2, movie_hour3=movie_hour3)


@app.route("/seats", methods=["POST", "GET"])
def seats():
    if request.method == "POST":
        return render_template("seats.html")
    else:
        return render_template("seats.html")

@app.route('/payment', methods=['POST'])
def payment():

    x = request.form.get("total")
    print(x)
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
                "total": x,
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
