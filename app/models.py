from app import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import  relationship
import enum
from flask_login import UserMixin
from datetime import datetime, date, time
class UserRoleEnum(enum.Enum):
    CUSTOMER = 1
    STAFF = 2
    ADMIN = 3

class AirportRole(enum.Enum):
    DEPARTURE = 1
    ARRIVAL = 2
    INTERMEDIATE = 3

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    avatar = Column(String(100), default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.CUSTOMER)
    joined_date = Column(DateTime, default=datetime.now())
    def __str__(self):
        return self.firstname

class Customer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User', uselist=False)
    ticket = relationship('Ticket', backref='Customer', lazy=True)
    def __str__(self):
        return self.user_id.name

class Staff(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User', uselist=False)
    flight_schedules = relationship("FlightSchedule", backref='Staff', lazy=True)

class Admin(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User', uselist=False)
    Stats = relationship('Stats', backref='Admin', lazy=True)

class Airport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    airport_address = Column(String(50), nullable=False)
    routes = relationship("RoutesInfo", backref="Airport", lazy=True)
    def __str__(self):
        return self.name

class Stats(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey(Admin.id), nullable=False)
    revenue = Column(Float, nullable=False)
    num_of_flights = Column(Integer, nullable=False)
    ratio = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    total_revenue = Column(Float, nullable=False)
    routes = relationship('Routes', backref='Stats', lazy=True)


class Routes(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    stats_id = Column(Integer, ForeignKey(Stats.id), nullable=False)
    flights = relationship('Flight', backref='Routes', lazy=True)
    airport = relationship("RoutesInfo", backref="Routes")

    def __str__(self):
        return self.name

class RoutesInfo(db.Model):
    airport_id = Column(Integer, ForeignKey(Airport.id), primary_key=True)
    routes_id = Column(Integer, ForeignKey(Routes.id), primary_key=True)
    airport_role = Column(Enum(AirportRole), nullable=False)
    stop_time = Column(Float, nullable=True)
    note = Column(String(500), nullable=True)

class Plane(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    flight = relationship('Flight', backref='Plane', lazy=True)
    seats = relationship('Seat', backref='Plane', lazy=True)
    def __str__(self):
        return self.name



# default value for empty ticket
def default_value(column_name):
    def default(context):
        return context.get_current_parameters()[column_name]
    return default


class FlightSchedule(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_details = relationship("FlightDetails", backref='FlightSchedule', lazy=True)
    staff = Column(Integer, ForeignKey(Staff.id), nullable=False)

class Flight(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    routes_id = Column(Integer, ForeignKey(Routes.id), nullable=False)
    flight_detail_id = relationship("FlightDetails", backref="Flight", uselist=False)
    tickets = relationship('Ticket', backref='Flight', lazy=True)
    flight_name = db.Column(db.String(64), unique=True)

class FlightDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False, unique=True)
    flight_schedule_id = Column(Integer, ForeignKey(FlightSchedule.id), nullable=False)
    time = Column(DateTime, nullable=False)
    flight_duration = Column(Float, nullable=False)
    num_of_seats_1st_class = Column(Integer, nullable=False)
    num_of_seats_2st_class = Column(Integer, nullable=False)
    num_of_empty_seats_1st_class = Column(Integer, default=default_value('num_of_seats_1st_class'), nullable=False)
    num_of_empty_seats_2st_class = Column(Integer, default=default_value('num_of_seats_2st_class'), nullable=False)

    def __str__(self):
        return f'Chi tiết chuyến bay có mã {self.flight_id}'

class FareClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    tickets = relationship('Ticket', backref='FareClass', lazy=True)
    def __str__(self):
        return self.name

class Seat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    fare_class_id = Column(Integer, ForeignKey(FareClass.id), nullable=False)
    ticket = relationship("Ticket", backref="Seat", uselist=False)
    def __str__(self):
        return self.name

class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    fare_class_id = Column(Integer, ForeignKey(FareClass.id), nullable=False)
    booking_date = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    seat = Column(Integer, ForeignKey(Seat.id), nullable=False, unique=True)

# class Rule(db.Model):
#     num_of_airport = Column(Integer, nullable=False)
#     minimum_duration = Column(Integer, nullable=False)
#     num_of_intermediate_airport = Column(Integer, nullable=False)
#     max_stoptime = Column(Float, nullable=False)
#     min_stoptime = Column(Float, nullable=False)
#     num_of_seats_1st_class = Column(Integer, nullable=False)
#     num_of_seats_2st_class = Column(Integer, nullable=False)
#     price_of_seats_1st_class = Column(Float, nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # user1 = User(last_name='Nguyen Van', first_name='A', phone='0931825412', address='111 van troi',
        #              email='vana@gmail.com')
        # user2 = User(last_name='Nguyen Van', first_name='B', phone='0731825412', address='112 van troi',
        #              email='vanb@gmail.com')
        # user3 = User(last_name='Nguyen Van', first_name='C', phone='0831825412', address='113 van troi',
        #              email='vanc@gmail.com')
        # db.session.add_all([user1, user2, user3])
        # db.session.commit()
        #
        # customer1 = Customer(user_id=user1.id)
        # db.session.add(customer1)
        # db.session.commit()
        #
        # staff1 = Staff(user_id=user2.id, password='123')
        # db.session.add(staff1)
        # db.session.commit()
        #
        # admin1 = Admin(user_id=user3.id, password='123')
        # db.session.add(admin1)
        # db.session.commit()
        #
        # airport1 = Airport(name='Noi Bai', airport_address='Ha Noi')
        # airport2 = Airport(name='Tan Son Nhat', airport_address='TP Ho Chi Minh')
        # airport3 = Airport(name='Can Tho', airport_address='Can Tho')
        # airport4 = Airport(name='Da Nang', airport_address='Da Nang')
        # db.session.add_all([airport1,airport2,airport3,airport4])
        # db.session.commit()
        #
        #
        # stats1 = Stats(admin_id=1, revenue=1000000, num_of_flights=121, ratio=80, month=3, total_revenue=59000000)
        # stats2 = Stats(admin_id=1, revenue=2000000, num_of_flights=122, ratio=70, month=4, total_revenue=60000000)
        # stats3 = Stats(admin_id=1, revenue=3000000, num_of_flights=123, ratio=60, month=5, total_revenue=61000000)
        # stats4 = Stats(admin_id=1, revenue=4000000, num_of_flights=124, ratio=90, month=6, total_revenue=62000000)
        # db.session.add_all([stats1,stats2,stats3,stats4])
        # db.session.commit()
        #
        # routes1 = Routes(name='Ha Noi - TP HCM', stats_id=1)
        # routes2 = Routes(name='Can Tho - TP HCM', stats_id=3)
        # routes3 = Routes(name='Da Nang - TP HCM', stats_id=4)
        # routes4 = Routes(name='TP HCM - Ha Noi', stats_id=2)
        # db.session.add_all([routes1,routes2,routes3,routes4])
        # db.session.commit()
        #
        # routes_info1 = RoutesInfo(airport_id=1,routes_id=1, airport_role=AirportRole.DEPARTURE)
        # routes_info2 = RoutesInfo(airport_id=2, routes_id=1, airport_role=AirportRole.ARRIVAL)
        # routes_info3 = RoutesInfo(airport_id=3, routes_id=2, airport_role=AirportRole.DEPARTURE)
        # routes_info4 = RoutesInfo(airport_id=2, routes_id=2, airport_role=AirportRole.ARRIVAL)
        # routes_info5 = RoutesInfo(airport_id=4, routes_id=3, airport_role=AirportRole.DEPARTURE)
        # routes_info6 = RoutesInfo(airport_id=2, routes_id=3, airport_role=AirportRole.ARRIVAL)
        # routes_info7 = RoutesInfo(airport_id=2, routes_id=4, airport_role=AirportRole.DEPARTURE)
        # routes_info8 = RoutesInfo(airport_id=1, routes_id=4, airport_role=AirportRole.ARRIVAL)
        # db.session.add_all([routes_info1,routes_info2,routes_info3,routes_info4,routes_info5,routes_info6])
        # db.session.commit()
        #
        # plane1 = Plane(name='VietNam Airlines')
        # plane2 = Plane(name='Vietjet Air')
        # plane3 = Plane(name='Jetstar Pacific')
        # plane4 = Plane(name='Bamboo Airways')
        # db.session.add_all([plane1,plane2,plane3,plane4])
        # db.session.commit()
        #
        #
        # flight_schedule1 = FlightSchedule(staff=1)
        # db.session.add(flight_schedule1)
        # db.session.commit()
        #
        #
        # flight1 = Flight(plane_id=1, routes_id=1, flight_name='VN007')
        # flight2 = Flight(plane_id=2, routes_id=2, flight_name='VN008')
        # flight3 = Flight(plane_id=3, routes_id=3, flight_name='VN009')
        # flight4 = Flight(plane_id=4, routes_id=4, flight_name='VN006')
        # db.session.add_all([flight1,flight2,flight3,flight4])
        # db.session.commit()
        #
        # flight_details1 = FlightDetails(flight_id=1, time=datetime(2024,5,9,11,00,00),
        #                                flight_duration=6.5, num_of_seats_1st_class = 100
        #                                , num_of_seats_2st_class=50, flight_schedule_id=1)
        # flight_details2 = FlightDetails(flight_id=2, time=datetime(2024,6,9,10,00,00),
        #                                 flight_duration=11.2, num_of_seats_1st_class=100
        #                                 , num_of_seats_2st_class=50, flight_schedule_id=1)
        # flight_details3 = FlightDetails(flight_id=3, time=datetime(2024,6,12,12,00,00),
        #                                 flight_duration=8, num_of_seats_1st_class=100
        #                                 , num_of_seats_2st_class=50,  flight_schedule_id=1)
        # flight_details4 = FlightDetails(flight_id=4, time=datetime(2024,6,15,12,00,00),
        #                                 flight_duration=9, num_of_seats_1st_class=100
        #                                 , num_of_seats_2st_class=50, flight_schedule_id=1)
        # db.session.add_all([flight_details1,flight_details2,flight_details3,flight_details4])
        # db.session.commit()
        #
        # fareclass1 = FareClass(name = 'Thuong Gia', price=1000000)
        # fareclass2 = FareClass(name='Pho Thong', price=500000)
        # db.session.add_all([fareclass1,fareclass2])
        # db.session.commit()
        # #
        # seat1 = Seat(name='Ghe 1', plane_id=1, fare_class_id=1)
        # seat2 = Seat(name='Ghe 2', plane_id=1, fare_class_id=2)
        # seat3 = Seat(name='Ghe 3', plane_id=2, fare_class_id=1)
        # seat4 = Seat(name='Ghe 4', plane_id=2, fare_class_id=2)
        # db.session.add_all([seat1,seat2,seat3,seat4])
        # db.session.commit()
        # #
        # ticket1 = Ticket(flight_id=1,  fare_class_id=1, customer_id=1, seat=1)
        # ticket2 = Ticket(flight_id=2, fare_class_id=2, customer_id=1, seat=2)
        # ticket3 = Ticket(flight_id=3, fare_class_id=1, customer_id=1, seat=3)
        # ticket4 = Ticket(flight_id=4, fare_class_id=2, customer_id=1, seat=4)
        # db.session.add_all([ticket1,ticket2,ticket3,ticket4])
        # db.session.commit()