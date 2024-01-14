import hashlib
from app.models import User, Airport, FlightDetails, AirportRole, Routes, RoutesInfo, Flight, Plane, FareClass, Seat
from app import app, db
from datetime import datetime
from sqlalchemy import and_, func


def get_user_by_id(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        return user


def add_user(surname=None, firstname=None, phone=None, address=None, email=None, password=None):
    if surname and firstname and phone and address and email and password:
        surname = surname.strip()
        firstname = firstname.strip()
        phone = phone.strip()
        address = address.strip()
        email = email.strip()
        password = password.strip()

        user = User(surname=surname, firstname=firstname, phone=phone, address=address, email=email, password=password)

        db.session.add(user)
        db.session.commit()


def check_user_existence(email=None, surname=None, firstname=None):
    if email:
        existing_user_email = User.query.filter_by(email=email.strip()).first()
        if existing_user_email:
            return False
    if surname and firstname:
        existing_user_name = User.query.filter_by(surname=surname.strip(), firstname=firstname.strip()).first()
        if existing_user_name:
            return False
    return True


def auth_user(email=None, password=None):
    if email and password:
        with app.app_context():
            user = User.query.filter_by(email=email.strip()).first()

            if user and user.password == password:
                return user


def get_departure_points():
    return Airport.query.all()

def get_flight_details(departure_airport_id, arrival_airport_id, departure_date, return_date, num_of_tickets):

    current_time = datetime.now()
    departure_date_input = datetime.strptime(departure_date, '%Y-%m-%d')

    routes_data = db.session.query(
        Routes.id.label('route_id'),
        Routes.name.label('route_name'),
        RoutesInfo.airport_id.label('routes_info_airport_id'),
        RoutesInfo.routes_id.label('routes_info_routes_id'),
        RoutesInfo.airport_role.label('routes_info_airport_role'),
        RoutesInfo.stop_time.label('routes_info_stop_time'),
        RoutesInfo.note.label('routes_info_note')
    ).join(RoutesInfo, Routes.id == RoutesInfo.routes_id).all()

    temp_route_1 =[]
    temp_route_2 =[]
    for x in routes_data:
        if x.routes_info_airport_id == int(departure_airport_id) and x.routes_info_airport_role == AirportRole.DEPARTURE:
            temp_route_1.append(x)
        if x.routes_info_airport_id == int(arrival_airport_id) and x.routes_info_airport_role == AirportRole.ARRIVAL:
            temp_route_2.append(x)

    route_id = None
    for x in temp_route_1:
        for y in temp_route_2:
            if x.route_id == y.route_id:
                route_id = x.route_id
                break

    flights = (db.session.query(
                Routes.id.label('route_id'),
                Routes.name.label('route_name'),
                RoutesInfo.airport_id.label('routes_info_airport_id'),
                RoutesInfo.routes_id.label('routes_info_routes_id'),
                RoutesInfo.airport_role.label('routes_info_airport_role'),
                RoutesInfo.stop_time.label('routes_info_stop_time'),
                RoutesInfo.note.label('routes_info_note'),
                Flight.id.label('flight_id'),
                Flight.plane_id.label('flight_plane_id'),
                Flight.routes_id.label('flight_routes_id'),
                Flight.flight_name.label('flight_name'),
                FlightDetails.id.label('flight_details_id'),
                FlightDetails.flight_id.label('flight_details_flight_id'),
                FlightDetails.flight_schedule_id.label('flight_details_flight_schedule_id'),
                FlightDetails.time.label('flight_details_time'),
                FlightDetails.flight_duration.label('flight_details_duration'),
                FlightDetails.num_of_seats_1st_class.label('flight_details_seats_1st_class'),
                FlightDetails.num_of_seats_2st_class.label('flight_details_seats_2st_class'),
                FlightDetails.num_of_empty_seats_1st_class.label('flight_details_empty_seats_1st_class'),
                FlightDetails.num_of_empty_seats_2st_class.label('flight_details_empty_seats_2nd_class')
            ).join(RoutesInfo, Routes.id == RoutesInfo.routes_id)
               .join(Flight, Routes.id == Flight.routes_id)
               .join(FlightDetails, Flight.id == FlightDetails.flight_id).all())

    tickets = db.session.query(
                Plane.id.label('plane_id'),
                Plane.name.label('plane_name'),
                FareClass.id.label('fare_class_id'),
                FareClass.name.label('fare_class_name'),
                FareClass.price.label('fare_class_price'),
                Seat.id.label('seat_id'),
                Seat.name.label('seat_name'),
                Flight.id.label('flight_id'),
                Flight.plane_id.label('flight_plane_id'),
                Flight.routes_id.label('flight_routes_id'),
                Flight.flight_name.label('flight_name')
            ).join(Seat, Plane.id == Seat.plane_id) \
                .join(FareClass, Seat.fare_class_id == FareClass.id) \
                .join(Flight, Plane.id == Flight.plane_id).all()

    departure_flight_data = []
    arrival_flight_data = []
    ticket_info =[]

    if route_id:
        for flight in flights:
            if flight.routes_info_airport_id == route_id and flight.routes_info_airport_role == AirportRole.DEPARTURE and flight.flight_details_time.date() == departure_date_input.date():
                departure_flight_data.append(flight)
            if flight.routes_info_airport_id == route_id and flight.routes_info_airport_role == AirportRole.ARRIVAL and flight.flight_details_time.date() == departure_date_input.date():
                arrival_flight_data.append(flight)

    for flight in departure_flight_data:
        for i in range(0, len(tickets)):
            if flight.flight_id == tickets[i].flight_id:
                ticket_info.append(tickets[i])

    return departure_flight_data, arrival_flight_data, ticket_info

def add_user(lastname, firstname, phone, address, email):
    new_user = User(last_name=lastname, first_name=firstname, phone=phone, address=address,
                 email=email)
    db.session.add(new_user)
    db.session.commit()

# class Ticket(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
#     fare_class_id = Column(Integer, ForeignKey(FareClass.id), nullable=False)
#     booking_date = Column(DateTime, default=datetime.now())
#     customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
#     seat = Column(Integer, ForeignKey(Seat.id), nullable=False, unique=True)


# class Seat(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
#     fare_class_id = Column(Integer, ForeignKey(FareClass.id), nullable=False)
#     ticket = relationship("Ticket", backref="Seat", uselist=False)
#     def __str__(self):
#         return self.name

# class Customer(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
#     User = relationship('User', uselist=False)
#     ticket = relationship('Ticket', backref='Customer', lazy=True)
#     def __str__(self):
#         return self.user_id.name

def add_customer():
    pass

def seat(name, plane_id, fare_class_id):
    pass

def add_ticket(flight_id, fare_class_id, customer_id, seat):
    pass
