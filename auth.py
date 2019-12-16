# File containing the "auth" blueprint. All routes related to user authentication
# can be found here
from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import Users
from . import db
import cgi
import datetime

# Defining the auth blueprint
auth = Blueprint('auth', __name__)
# The following registration code is used on user registration.
reg_code = 'V3RD396'

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # The cgi.escape function allows you to escape html characters and avoid SQL injection
        email = cgi.escape(request.form.get('email'), quote=True)
        password = cgi.escape(request.form.get('password'), quote=True)
        remember = True if request.form.get('remember') else False

        # find the user with the e-mail provided
        user = Users.query.filter_by(user_name=email).first()

        # If the user is not found or the password doesn't match, flash an error.
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        # The function login_user creates a user session
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))
    else:
        return render_template('login.html')



@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        now = datetime.datetime.now()
        email = cgi.escape(request.form.get('email'), quote=True)
        code = cgi.escape(request.form.get('code'), quote=True)
        password = cgi.escape(request.form.get('password'), quote=True)
        repassword = cgi.escape(request.form.get('repeat-password'), quote=True)
        user = Users.query.filter_by(user_name=email).first()

        # if a user already uses the e-mail address, then flash an error
        if user:
            flash('Email address already exists.')
            return redirect(url_for('auth.register'))

        # if the two passwords don't match, flash an error.
        if password != repassword:
            flash('Passwords provided do not match.')
            return redirect(url_for('auth.register'))

        # if the registration code doesn't match the hardcoded value, flash an error.
        if code != reg_code:
            flash('Incorrect registration code.')
            return redirect(url_for('auth.register'))

        # If all validation works, then create a new user.
        new_user = Users(user_name=email, password=generate_password_hash(password, method='sha256'), add_date=now.strftime("%Y-%m-%d %H:%M"))

        # Persist changes on the database.
        db.session.add(new_user)
        db.session.commit()

        # Login the new user.
        login_user(new_user)
        return redirect(url_for('main.index'))
    else:
        return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    # The function logout_user terminates the user sesion.
    logout_user()
    return redirect(url_for('auth.login'))