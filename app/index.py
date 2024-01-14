
from flask_login import login_user, logout_user
from app import dao, app, login, db
from flask import render_template, request, redirect, url_for, flash
from app.models import AirportRole, FlightDetails, RoutesInfo, Flight, Routes


@app.route('/')
def home():
    return render_template('index.html')



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

@app.route('/ticket')
def ticket():
    airport_id = request.args.get("airport_id")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    fli = dao.get_flight_details_schedule(airport_id=airport_id, from_date=from_date, to_date=to_date)
    air = dao.read_airports()

    return render_template("ticket.html",
                           flights=fli, airports=air)

# logging.basicConfig(filename='error.log', level=logging.ERROR)
@app.route('/ticket/add', methods=["GET", "POST"])
def add_or_update_ticket():
    err = " "
    if request.method == "POST":
        #----- Routes Info
        airport_id = request.form.get('routes_info_airport_id')
        routes_id = request.form.get('routes_info_routes_id')
        airport_role = request.form.get('routes_info_airport_role')

        #----- Flight Details
        flight_id = request.form.get('flight_details_flight_id')
        flight_schedule_id = request.form.get('flight_details_flight_schedule_id')
        time = request.form.get('flight_details_time')
        flight_duration = request.form.get('flight_details_duration', 3.2)
        num_of_seats_1st_class = request.form.get('flight_details_seats_1st_class', 0)
        num_of_seats_2st_class = request.form.get('flight_details_seats_2st_class', 0)

        if airport_role in AirportRole.__members__:
            airport_role = AirportRole[airport_role]



        if dao.add_flight_schedule( airport_id= airport_id,
                                    routes_id=routes_id,
                                    airport_role=airport_role,
                                    flight_id = flight_id,
                                    flight_schedule_id = flight_schedule_id,
                                    time=time,
                                    flight_duration=flight_duration,
                                    num_of_seats_1st_class = num_of_seats_1st_class,
                                    num_of_seats_2st_class = num_of_seats_2st_class):

            return redirect(url_for("ticket"))
        else:
            err = "Something wrong !!!"

    flight_details = FlightDetails.query.get(id)

    return render_template("ticket-add.html",
                           routes=dao.read_routes(),
                           planes=dao.read_planes(),
                           airports=dao.read_airports(),
                           flights=dao.read_flights(),
                           flight_details=dao.get_flight_details_schedule(),
                           flight_schedules = dao.read_flight_schedules(),
                           staffs = dao.read_staffs(),
                           flight = flight_details,
                           err=err)

@app.route('/ticket/update/flight = <int:flight_details_id>', methods=['GET', 'POST'])
def update_ticket_by_id(flight_details_id):

    flight_detail = FlightDetails.query \
        .join(Flight, FlightDetails.flight_id == Flight.id) \
        .join(Routes, Flight.routes_id == Routes.id) \
        .join(RoutesInfo, Routes.id == RoutesInfo.routes_id) \
        .filter(FlightDetails.id == flight_details_id) \
        .first()

    routes_info = RoutesInfo.query.join(FlightDetails, RoutesInfo.routes_id == FlightDetails.id) \
                                  .filter(FlightDetails.id == flight_details_id) \
                                  .first()

    if request.method == 'POST':
            if routes_info:
                # Update routes_info
                routes_info.airport_id = request.form.getlist('routes_info_airport_id')[0]
                routes_info.routes_id = request.form.getlist('routes_info_routes_id')[0]
                routes_info.airport_role = request.form.getlist('routes_info_airport_role')[0]
                db.session.commit()

            if flight_detail:
                # Update flight_detail
                flight_detail.flight_id = request.form.getlist('flight_details_flight_id')[0]
                flight_detail.flight_schedule_id = request.form.getlist('flight_details_flight_schedule_id')[0]
                flight_detail.time = request.form.getlist('flight_details_time')[0]
                flight_detail.flight_duration = request.form.getlist('flight_details_duration')[0]
                flight_detail.num_of_seats_1st_class = request.form.getlist('flight_details_seats_1st_class')[0]
                flight_detail.num_of_seats_2st_class = request.form.getlist('flight_details_seats_2st_class')[0]

                db.session.commit()

            return redirect(url_for('ticket'))

    return render_template("ticket-update.html",
                           routes=dao.read_routes(),
                           planes=dao.read_planes(),
                           airports=dao.read_airports(),
                           flights=dao.read_flights(),
                           flight_details=dao.get_flight_details_schedule(),
                           flight_schedules=dao.read_flight_schedules(),
                           staffs=dao.read_staffs(),
                           flight=flight_detail,
                           routes_info=routes_info)


@app.route('/ticket/delete/<int:flight_details_id>', methods=['GET','POST'])
def delete_ticket_by_id(flight_details_id):
        flight_details = FlightDetails.query.filter_by(id=flight_details_id).first()

        if flight_details:
            db.session.delete(flight_details)
            db.session.commit()

            return redirect(url_for('ticket'))


if __name__ == '__main__':
    app.run(debug=True)
