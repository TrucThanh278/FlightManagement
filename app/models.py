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

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
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
class NhanVien(BaseModel, User):
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.NHANVIEN)
    # LichChuyenBay = relationship('LichChuyenBay', backref='NhanVien', lazy=True)
class SanBay(BaseModel):
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    TuyenBay = relationship('TuyenBay', backref='SanBay', lazy=True)

# class NguoiQuanTri(BaseModel):
#     ThongKeBaoCao = relationship('ThongKeBaoCao', backref='NguoiQuanTri', lazy=True)
class ThongKeBaoCao(BaseModel):
    # nguoiquantri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)
    doanhThu = Column(Float, nullable=False)
    soLuotBay = Column(Integer, nullable=False)
    tiLe = Column(Float, nullable=False)
    Thang = Column(Integer, nullable=False)
    tongDoanhTho = Column(Float, nullable=False)
    TuyenBay = relationship('TuyenBay', backref='ThongKeBaoCao', lazy=True)

class TuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    sanbay_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thongkebaocao_id = Column(Integer, ForeignKey(ThongKeBaoCao.id), nullable=False)
    ChuyenBay = relationship('ChuyenBay', backref='TuyenBay', lazy=True)

class SanBayTrungGian(BaseModel):
    sanbay_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    tuyenbay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    thoigianDung = Column(Float, nullable=False)
    ghiChu = Column(String(500), nullable=False)

class MayBay(BaseModel):
    name = Column(String(50), nullable=False)
    ChuyenBay = relationship('ChuyenBay', backref='MayBay', lazy=True)
    Ghe = relationship('Ghe', backref='MayBay', lazy=True)

# class NhanVien(BaseModel):
#     LichChuyenBay = relationship('LichChuyenBay', backref='NhanVien', lazy=True)
class LichChuyenBay(BaseModel):
    nhanvien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    ngayGio = Column(String(100), nullable=False)
    thoiGianBay = Column(Float, nullable=False)
    soLuongGheHang1 = Column(Integer, nullable=False)
    soLuongGheHang2 = Column(Integer, nullable=False)
    ChuyenBay = relationship('ChuyenBay', backref='LichChuyenBay', lazy=False)
class ChuyenBay(BaseModel):
    khoiHanh = Column(DateTime, nullable=False)
    maybay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    tuyenbay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    lichchuyenbay_id = Column(Integer, ForeignKey(LichChuyenBay.id), nullable=False)
    Ve = relationship('Ve', backref='ChuyenBay', lazy=True)

class ChiTietChuyenBay(BaseModel):
    lichchuyenbay_id = Column(Integer, ForeignKey(LichChuyenBay.id), nullable=False)
    sanbay_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanBayDen = Column(String(200), nullable=False)
    sanBayDi = Column(String(200), nullable=False)
    ghiChu = Column(String(500), nullable=False)

class HangGheVe (BaseModel):
    name = Column(String(50), nullable=False)
    Ghe = relationship('Ghe', backref='HangGheVe', lazy=True)
class Ghe(BaseModel):
    name = Column(String(50), nullable=False)
    hangGhe = Column(String(100), nullable=False)
    maybay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    hanggheve_id = Column(Integer, ForeignKey(HangGheVe.id), nullable=False)

# class KhachHang(BaseModel):
#     Ve = relationship('Ve', backref='KhachHang', lazy=True)
class Ve(BaseModel):
    chuyenbay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    gia = Column(Float, nullable=False)
    ngaybook = Column(DateTime, default=datetime.now())
    # khachhang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)





if __name__ == "__main__":
    with app.app_context():
        db.create_all()