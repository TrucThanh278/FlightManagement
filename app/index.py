from flask_login import login_user, logout_user
from app import dao, db, app, login
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        surname = request.form.get('surname')
        firstname = request.form.get('firstname')
        phone = request.form.get('phone')
        address = request.form.get('address')
        email = request.form.get('email')
        password = request.form.get('password')

        if not (surname and firstname and phone and address and email and password):
            flash('Please fill in all the fields', 'error')
            return redirect(url_for('register'))

        if not dao.check_user_existence(email=email, surname=surname, firstname=firstname):
            flash('User already exists. Please choose a different email or username.', 'error')
            return redirect(url_for('register'))

        dao.add_user(surname=surname, firstname=firstname, phone=phone, address=address, email=email, password=password)

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
            return redirect(url_for('home'))
        else:
            err_msg = "Invalid email or password."

    return render_template("login.html", err_msg=err_msg)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)