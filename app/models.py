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
    USER = 1
    ADMIN = 2
    NHANVIEN = 3

class User(BaseModel, UserMixin):
    surname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    joined_date = Column(DateTime, default=datetime.now())
    def __str__(self):
        return self.name
class KhachHang(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User')
    Ve = relationship('Ve', backref='KhachHang', lazy=True)
class NhanVien(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User')
    ChiTietChuyenBay = relationship('ChiTietChuyenBay', backref='NhanVien', lazy=True)
class NguoiQuanTri(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    User = relationship('User')
    ThongKeBaoCao = relationship('ThongKeBaoCao', backref='NguoiQuanTri', lazy=True)

class SanBay(BaseModel):
    name = Column(String(50), nullable=False)
    TuyenBay = relationship('TuyenBay', backref='SanBay', lazy=True)
    def __str__(self):
        return self.name


class ThongKeBaoCao(BaseModel):
    nguoiquantri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)
    doanhThu = Column(Float, nullable=False)
    soLuotBay = Column(Integer, nullable=False)
    tiLe = Column(Float, nullable=False)
    Thang = Column(Integer, nullable=False)
    tongDoanhTho = Column(Float, nullable=False)
    TuyenBay = relationship('TuyenBay', backref='ThongKeBaoCao', lazy=True)
    def __str__(self):
        return self.name

class TuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    sanbay_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thongkebaocao_id = Column(Integer, ForeignKey(ThongKeBaoCao.id), nullable=False)
    ChuyenBay = relationship('ChuyenBay', backref='TuyenBay', lazy=True)
    def __str__(self):
        return self.name

class SanBayTrungGian(BaseModel):
    sanbay_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    tuyenbay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    thoigianDung = Column(Float, nullable=False)
    ghiChu = Column(String(500), nullable=False)
    def __str__(self):
        return self.name

class MayBay(BaseModel):
    name = Column(String(50), nullable=False)
    ChuyenBay = relationship('ChuyenBay', backref='MayBay', lazy=True)
    Ghe = relationship('Ghe', backref='MayBay', lazy=True)
    def __str__(self):
        return self.name
class ChuyenBay(BaseModel):
    khoiHanh = Column(DateTime, nullable=False)
    maybay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    tuyenbay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    Ve = relationship('Ve', backref='ChuyenBay', lazy=True)
    ten_chuyen_bay = db.Column(db.String(64), unique=True)
    chi_tiet = db.relationship('ChiTietChuyenBay', backref='ChuyeBbay', lazy='dynamic')
    def __str__(self):
        return self.name

class ChiTietChuyenBay(BaseModel):
    nhanvien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    ngayGio = Column(String(100), nullable=False)
    thoiGianBay = Column(Float, nullable=False)
    soLuongGheHang1 = Column(Integer, nullable=False)
    soLuongGheHang2 = Column(Integer, nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id))
    san_bay_di_id = Column(Integer, ForeignKey(SanBay.id))
    san_bay_den_id = Column(Integer, ForeignKey(SanBay.id))
    san_bay_di = relationship('SanBay', foreign_keys=[san_bay_di_id])
    san_bay_den = relationship('SanBay', foreign_keys=[san_bay_den_id])
    def __str__(self):
        return self.name

class HangVe (BaseModel):
    name = Column(String(50), nullable=False)
    Ve = relationship('Ve', backref='HangVe', lazy=True)
class Ghe(BaseModel):
    name = Column(String(50), nullable=False)
    maybay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    hangve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    def __str__(self):
        return self.name
class Ve(BaseModel):
    chuyenbay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hangve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    gia = Column(Float, nullable=False)
    ngaybook = Column(DateTime, default=datetime.now())
    khachhang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    def __str__(self):
        return self.name


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

