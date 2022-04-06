from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from .model import Users
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        # emailid = request.form['emailid']
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get("password2")

        new_user = Users.query.filter_by(username=username).first()

        if new_user:
            flash("Username already taken! Try again..", category='error')
        elif len(name) < 2:
            flash("Name must be greater than 1 character", category='error')
        elif password1 != password2:
            flash("Passwords does not match!", category='error')
        elif len(password1) < 7:
            flash("Pawssword must be greater than 7 characters", category='error')
        else:
            new_user = Users(name=name, username=username,
                             password=generate_password_hash(password1, method='sha256'))

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account creation successful.', category='success')

            return redirect(url_for('views.home'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully...", category='success')
                login_user(user, remember=True)
                return render_template('home.html', username=username)

            else:
                flash("Incorrect Password! Try again...", category='error')

        else:
            flash("Username does not exist! Check again...", category='error')

    return render_template('login.html')


@ auth.route('/signout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
