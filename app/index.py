from flask_login import login_user, logout_user
from app import dao, db, app, login
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import current_user
import json
import urllib.request
import urllib
import uuid
import requests
import hmac
import hashlib


@app.route('/')
def index():
    locations = dao.get_departure_points()

    return render_template('index.html', locations=locations)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        last_name = request.form.get('last-name')
        first_name = request.form.get('first-name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        email = request.form.get('email')
        password = request.form.get('password')

        if not (last_name and first_name and phone and address and email and password):
            flash('Please fill in all the fields', 'error')
            return redirect(url_for('register'))

        if not dao.check_user_existence(email=email, last_name=last_name, first_name=first_name):
            flash('User already exists. Please choose a different email or username.', 'error')
            return redirect(url_for('register'))

        dao.add_user(last_name=last_name, first_name=first_name, phone=phone, address=address, email=email, password=password)

        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    err_msg = ""
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = dao.auth_user(email=email, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('/'))
        else:
            err_msg = "Invalid email or password."

    return render_template("login.html", err_msg=err_msg)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/bookticket', methods=['POST'])
def find_ticket():
    departure_airport_id = request.form.get('departure')
    arrival_airport_id = request.form.get('destination')
    departure_date = request.form.get('departure-date')
    return_date = request.form.get('return-date')
    num_of_tickets = request.form.get('quantity-tickets')

    departure_flight_data, arrival_flight_data, ticket_info = dao.get_flight_details(departure_airport_id,
                                                                                     arrival_airport_id,
                                                                                     departure_date,
                                                                                     return_date,
                                                                                     num_of_tickets)
    return render_template("bookticket.html", departure_flight_data=departure_flight_data,
                           arrival_flight_data=arrival_flight_data, ticket_info=ticket_info,
                           num_of_tickets=num_of_tickets)


@app.route(
    '/load_form_passenger/<flight_id>/<plane_id>/<time>/<duration>/<fare_class_id>/<fare_class_price>/<num_of_tickets>')
def load_form_passenger(flight_id, plane_id, time, duration, fare_class_id, fare_class_price, num_of_tickets):
    ticket_info = {
        "flight_id": flight_id,
        "plane_id": plane_id,
        "time": time,
        "duration": duration,
        "fare_class_id": fare_class_id,
        "fare_class_price": fare_class_price,
        "num_of_tickets": num_of_tickets
    }

    session["ticket_info"] = ticket_info

    return render_template('passenger.html', flight_id=flight_id,
                           plane_id=plane_id, time=time, duration=duration, fare_class_id=fare_class_id,
                           fare_class_price=fare_class_price, num_of_tickets=num_of_tickets)


@app.route('/payments', methods=["GET", "POST"])
def payments():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')
    phone_number = request.form.get('phone-number')
    address = request.form.get('address')

    passenger_info = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "address": address
    }

    print(passenger_info)

    session["passenger"] = passenger_info

    return render_template('payment.html', session=session)

@app.route('/thanks', methods=["GET"])
def load_thanks_page():
    return render_template("thanks.html")

@app.route('/payUrl', methods=['GET'])
def handle_payments():
    # parameters send to MoMo get get payUrl
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "Thanh toan qua MoMo"
    redirectUrl = "http://127.0.0.1:5000/thanks"
    ipnUrl = "http://127.0.0.1:5000/momo_ipn"
    amount = "10000"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "payWithATM"
    extraData = ""  # pass empty value or Encode base64 JsonString
    # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
    # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
    # &requestType=$requestType
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

    # puts raw signature
    print("--------------------RAW SIGNATURE----------------")
    print(rawSignature)
    # signature
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    print("--------------------SIGNATURE----------------")
    print(signature)

    # json object send to MoMo endpoint

    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    print("--------------------JSON REQUEST----------------\n")
    data = json.dumps(data)
    print(data)

    clen = len(data)
    response = requests.post(endpoint, data=data,
                             headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

    # f.close()
    print("--------------------JSON response----------------\n")
    print(response.json())

    print(response.json()['payUrl'])

    try:
        response = requests.post(endpoint, data=data,
                                 headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

        # Xử lý phản hồi từ API
        if response.status_code == 200:
            data = response.json()
            user_ino = session.get("passenger")
            dao.add_user(user_ino.get("last_name"),
                         user_ino.get("first_name"),
                         user_ino.get("phone_number"),
                         user_ino.get("address"),
                         user_ino.get("email"))

            return redirect(data.get('payUrl'))
        else:
            return f'Error: {response.status_code}'
    except Exception as e:
        return f'Error: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)
