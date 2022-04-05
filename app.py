from ast import Return
from enum import unique
from unittest import result
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Users(db.Model):
    username = db.Column(db.String,  primary_key=True,
                         nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f'{self.username} --> {self.password}'


@app.route('/')
def welcome():
    return render_template('login.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    user = Users.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            return render_template('home.html', username=username)
    return render_template('login.html', result="Invalid Credentials", warningbg='alert-warning')


@app.route('/newuser', methods=["GET", "POST"])
def newuser():
    return render_template('register.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password and username:
            new_user = Users(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html', result="Registration successfull", warningbg='alert-success')
        else:
            return render_template('register.html', result="Please fill all the boxes", warningbg='alert-danger')


if __name__ == '__main__':
    app.run(debug=False)
