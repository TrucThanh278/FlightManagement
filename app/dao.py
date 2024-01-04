import hashlib

from app.models import User
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
