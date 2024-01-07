from app import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import  relationship
import enum
from flask_login import UserMixin
from datetime import datetime, date, time

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRoleEnum(enum.Enum):
    CUSTOMER = 1
    STAFF = 2
    ADMIN = 3

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.CUSTOMER)
    joined_date = Column(DateTime, default=datetime.now())
    def __str__(self):
        return self.firstname

class Customer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User')
    Ve = relationship('Ticket', backref='Customer', lazy=True)
    def __str__(self):
        return self.user_id.name

class Staff(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User')
    flight_details = relationship('FlightDetails', backref='Staff', lazy=True)
    flight_schedules = relationship("FlightSchedule", backref='Staff', lazy=True)

class Admin(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User')
    Stats = relationship('Stats', backref='Admin', lazy=True)

class Airport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    airport_address = Column(String(50), nullable=False)
    routes = relationship('Routes', backref='Airport', lazy=True)
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
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    stats_id = Column(Integer, ForeignKey(Stats.id), nullable=False)
    flights = relationship('Flight', backref='Routes', lazy=True)
    def __str__(self):
        return self.name

class IntermediateAirport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    routes_id = Column(Integer, ForeignKey(Routes.id), nullable=False)
    stop_time = Column(Float, nullable=False)
    note = Column(String(500), nullable=False)
    def __str__(self):
        return self.name

class Plane(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    flight = relationship('Flight', backref='Plane', lazy=True)
    seats = relationship('Seat', backref='Plane', lazy=True)
    def __str__(self):
        return self.name

class Flight(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DateTime, nullable=False)
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    routes_id = Column(Integer, ForeignKey(Routes.id), nullable=False)
    tickets = relationship('Ticket', backref='Flight', lazy=True)
    flight_name = db.Column(db.String(64), unique=True)
    details = db.relationship('FlightDetails', backref='Flight', lazy='dynamic')
    def __str__(self):
        return f'Chuyến bay có mã: {self.id}, tên chuyến bay: {self.flight_name}'
class FlightSchedule(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_details = relationship("FlightDetails", backref='FlightSchedule', lazy=True)
    staff = Column(Integer, ForeignKey(Staff.id), nullable=False)

class FlightDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)
    time = Column(String(100), nullable=False)
    flight_duration = Column(Float, nullable=False)
    num_of_seats_1st_class = Column(Integer, nullable=False)
    num_of_seats_2st_class = Column(Integer, nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id))
    departure_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    arrival_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    flight_schedule_id = Column(Integer, ForeignKey(FlightSchedule.id), nullable=False)
    departure_airport = relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = relationship('Airport', foreign_keys=[arrival_airport_id])
    def __str__(self):
        return f'Chi tiết chuyến bay có mã {self.flight_id}'


class FareClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    tickets = relationship('Ticket', backref='FareClass', lazy=True)
    def __str__(self):
        return self.name

class Seat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    fare_class_id = Column(Integer, ForeignKey(FareClass.id), nullable=False)
    def __str__(self):
        return self.name

class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    fare_class_id = Column(Integer, ForeignKey(FareClass.id), nullable=False)
    price = Column(Float, nullable=False)
    booking_date = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # sb1 = SanBay(name='Sân bay Quốc tế Nội Bài')
        # sb2 = SanBay(name='Sân bay Quốc tế Tân Sơn Nhất')
        # sb3 = SanBay(name='Sân bay Quốc tế Cần Thơ')
        # sb4 = SanBay(name='Sân bay Cà Mau')
        # sb5 = SanBay(name='Sân bay Quốc tế Đà Nẵng')
        # db.session.add_all([sb1,sb2,sb3,sb4,sb5])
        # db.session.commit()


        # tkbc1 = ThongKeBaoCao(nguoiquantri_id = 2,doanhThu=1132312321,soLuotBay=4,tiLe=12,Thang=3,tongDoanhTho=21312312)
        # tkbc2 = ThongKeBaoCao(nguoiquantri_id = 2,doanhThu=2332312321, soLuotBay=10, tiLe=78, Thang=8, tongDoanhTho=37812312)
        # tkbc3 = ThongKeBaoCao(nguoiquantri_id = 2,doanhThu=5632312321, soLuotBay=15, tiLe=57, Thang=12, tongDoanhTho=51312312)
        # db.session.add_all([tkbc1,tkbc2,tkbc3])
        # db.session.commit()

        # tb1 = TuyenBay(name='Ha Noi - TP HCM', sanbay_id=1, thongkebaocao_id=2)
        # tb2 = TuyenBay(name='CanTho - TP HCM', sanbay_id=3, thongkebaocao_id=1)
        # tb3 = TuyenBay(name='DaNang - TP HCM', sanbay_id=5, thongkebaocao_id=1)
        # tb4 = TuyenBay(name='CaMau - TP HCM', sanbay_id=4, thongkebaocao_id=3)
        # tb5 = TuyenBay(name='Da Nang - Ha Noi', sanbay_id=5, thongkebaocao_id=2)
        # db.session.add_all([tb1, tb2, tb3, tb4, tb5])
        # db.session.commit()
        #
        # mb1 = MayBay(name='VietNamAirlines')
        # db.session.add_all([mb1])
        # db.session.commit()
        #
        #
        # cb1 = ChuyenBay(khoiHanh=datetime(2024, 1, 7, 10, 55, 00), maybay_id=1, tuyenbay_id=2)
        # cb2 = ChuyenBay(khoiHanh=datetime(2024, 1, 8, 11, 55, 00), maybay_id=1, tuyenbay_id=1)
        # cb3 = ChuyenBay(khoiHanh=datetime(2024, 1, 9, 2, 00, 00), maybay_id=1, tuyenbay_id=4)
        # cb4 = ChuyenBay(khoiHanh=datetime(2024, 1, 10, 3, 00, 00), maybay_id=1, tuyenbay_id=5)
        # db.session.add_all([cb1, cb2, cb3, cb4])
        # db.session.commit()
        #
        # ctcb1 = ChiTietChuyenBay(ngayGio='2024/1/7 - 10h55', thoiGianBay=6, soLuongGheHang1=50, soLuongGheHang2=30, chuyen_bay_id = 1, san_bay_di_id=2, san_bay_den_id=1)
        # ctcb2 = ChiTietChuyenBay(ngayGio='2024/1/8 - 11h55', thoiGianBay=3, soLuongGheHang1=50, soLuongGheHang2=30, chuyen_bay_id = 3, san_bay_di_id=2, san_bay_den_id=4)
        # ctcb3 = ChiTietChuyenBay(ngayGio='2024/1/9 - 2h', thoiGianBay=7,soLuongGheHang1=50, soLuongGheHang2=30 , chuyen_bay_id = 2, san_bay_di_id=2, san_bay_den_id=3)
        # ctcb4 = ChiTietChuyenBay(ngayGio='2024/1/10 - 3h', thoiGianBay=2, soLuongGheHang1=50, soLuongGheHang2=30, chuyen_bay_id = 4, san_bay_di_id=2, san_bay_den_id=5)
        # ctcb5 = ChiTietChuyenBay(ngayGio='2024/1/8 - 11h55',thoiGianBay=10, soLuongGheHang1=50, soLuongGheHang2=30, chuyen_bay_id = 1,san_bay_di_id=2, san_bay_den_id=1)
        # db.session.add_all([ctcb1, ctcb2, ctcb3, ctcb4, ctcb5])
        # db.session.commit()
        #
        # hv1 = HangVe(name='Thuong Gia')
        # hv2 = HangVe(name='Pho Thong')
        # db.session.add_all([hv1, hv2])
        # db.session.commit()
        #
        # g1 = Ghe(name='ghe 1', maybay_id=1 , hanggheve_id= 1)
        # g2 = Ghe(name='ghe 2', maybay_id=1, hanggheve_id=1)
        # g3 = Ghe(name='ghe 3', maybay_id=1, hanggheve_id=1)
        # g4 = Ghe(name='ghe 4', maybay_id=1, hanggheve_id=2)
        # g5 = Ghe(name='ghe 5', maybay_id=1, hanggheve_id=2)
        # db.session.add_all([g1,g2,g3,g4,g5])
        # db.session.commit()
        #
        # v1 = Ve(chuyenbay_id= 1, hangve_id=1, gia=10000000)
        # v2 = Ve(chuyenbay_id=2, hangve_id=1,gia=12000000)
        # v3 = Ve(chuyenbay_id=3, hangve_id=2,gia=14000000)
        # v4 = Ve(chuyenbay_id=4, hangve_id=2,gia=18000000)
        # db.session.add_all([v1,v2,v3,v4])
        # db.session.commit()