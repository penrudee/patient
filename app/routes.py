from app import app
from app.models import *
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user , logout_user, login_required
from werkzeug.urls import url_parse

import datetime 


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form =LoginForm()
    if form.validate_on_submit():
        user = Pharmacist.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',
                            title='Login',
                            form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Pharmacist(username=form.username.data, email=form.email.data, create_time=datetime.datetime.now())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html",
                            title="Home")

@app.route('/allpatients')
@login_required
def allpatients():
    pts = Patient.query.order_by(Patient.id.desc()).filter_by(pharmacist_id=current_user.id)
    return render_template("allpatients.html",
                            title="ผู้ป่วยทั้งหมด",
                            pts=pts)


@app.route("/addpatient",methods=['POST'])
@login_required
def addpatient():
    if request.method =='POST':
        phone = request.form.get("add_telephone")
        fname = request.form.get("add_first_name")
        lname = request.form.get("add_last_name")
        nation_id =request.form.get("add_nation_id")
        pt = Patient()
        pt.firstname = fname
        pt.lastname = lname 
        pt.phone_no = phone 
        pt.create_time = datetime.datetime.now()
        pt.pharmacist_id = current_user.id 
        pt.nation_id = nation_id
        db.session.add(pt)
        db.session.commit()
        flash("เพิ่มผู้ป่วยใหม่แล้ว!",'success')
    return redirect(url_for('index'))