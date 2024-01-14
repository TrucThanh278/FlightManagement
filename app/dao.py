from datetime import datetime

from flask import redirect, url_for

from app.models import (User, FlightDetails, Airport, Flight, FlightSchedule, Staff, RoutesInfo, Routes, Plane)
from sqlalchemy import exc
from app import app, db
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

        user = User(surname=surname, firstname=firstname, phone=phone,
                    address=address, email=email, password=password)

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

def get_flight_details(airport_id = None, from_date =None, to_date=None):

    flights = db.session.query(
                    Routes.id.label('route_id'),
                    Routes.name.label('route_name'),
                    Routes.stats_id.label('route_stats_id'),
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
                ).join(RoutesInfo, Routes.id == RoutesInfo.routes_id)\
                 .join(Flight, Routes.id == Flight.routes_id)\
                 .join(FlightDetails, Flight.id == FlightDetails.flight_id)

    if airport_id:
        flights = flights.filter(RoutesInfo.airport_id == airport_id)

    if from_date and to_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')  # Remove spaces around the time
        to_date = datetime.strptime(to_date, '%Y-%m-%d')  # Remove spaces around the time
        flights = flights.filter(FlightDetails.time.between(from_date, to_date))
        print(flights)

    return flights.all()

def read_planes():
    return Plane.query.all()
def read_airports():
    return Airport.query.all()

def read_flights():
    return Flight.query.all()
def read_flight_schedules():
    return FlightSchedule.query.all()

def read_staffs():
    return Staff.query.all()
def read_routes():
    return Routes.query.all()

def add_flight_schedule(
                        airport_id = None, routes_id =None,airport_role=None
                        , flight_id = None,
                        flight_schedule_id= None,
                        time= None,flight_duration=None, num_of_seats_1st_class= None,
                        num_of_seats_2st_class= None):

    if ( airport_id and  routes_id and airport_role and
            flight_id and flight_schedule_id and
            time and flight_duration and
            num_of_seats_1st_class and num_of_seats_2st_class ):

        #-----Routes Info
        airport_id = airport_id
        routes_id  = routes_id
        airport_role = airport_role
        # ----Flight details
        flight_id = flight_id
        flight_schedule_id = flight_schedule_id
        time = time
        flight_duration = flight_duration
        num_of_seats_1st_class = num_of_seats_1st_class
        num_of_seats_2st_class = num_of_seats_2st_class


        routes_info = RoutesInfo( airport_id = airport_id,
                                    routes_id  = routes_id ,
                                  airport_role=airport_role)
        db.session.add(routes_info)
        db.session.commit()

        flight_details = FlightDetails(flight_id = flight_id,
                                      flight_schedule_id = flight_schedule_id,
                                       time=time,
                                    flight_duration = flight_duration,
                                    num_of_seats_1st_class = num_of_seats_1st_class,
                                       num_of_seats_2st_class=num_of_seats_2st_class)

        db.session.add(flight_details)
        db.session.commit()
        return redirect(url_for("ticket"))
def read_ticket_by_id(flight_detail_id):
    flights = db.session.query(
        Routes.id.label('route_id'),
        Routes.name.label('route_name'),
        Routes.stats_id.label('route_stats_id'),
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
    ).join(RoutesInfo, Routes.id == RoutesInfo.routes_id) \
        .join(Flight, Routes.id == Flight.routes_id) \
        .join(FlightDetails, Flight.id == FlightDetails.flight_id)

    for flight in flights:
        if flight.flight_details_id == flight_detail_id:
            return flight
    return None




