from app import app
from app.models import *
from flask import render_template, redirect, flash, url_for, request,jsonify
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user , logout_user, login_required
from werkzeug.urls import url_parse
from PIL import Image
from werkzeug.utils import secure_filename
import datetime 
import os 


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

@app.route('/showproduct')
@login_required
def showproduct():
    allproducts=Product.query.order_by(Product.id.desc())
    return render_template("showproduct.html",
                            title="All Product",
                            allproducts=allproducts)
@app.route('/addproduct',methods=['POST'])
@login_required
def addproduct():
    if request.method=='POST':
        p = Product()
        p.create_time = datetime.datetime.now()
        
        product_image = request.files['productImage']
        p.title = request.form.get("productName")
        p.body = request.form.get("productDetail")
        p.price=request.form.get("productPrice")
        p.unit = request.form.get("productUnit")
        p.contact = request.form.get("lineId")
        p.pharmacist_id=current_user.id 
        p.have_it = True 
         # Save image to disk
        image_name = secure_filename(product_image.filename)
        image_path = os.path.join(app.root_path, 'static', 'productImage', image_name)
        product_image.save(image_path)
        p.img = image_name
        db.session.add(p)
        db.session.commit()
        flash("Add Product","success")



    return redirect(url_for('showproduct'))

@app.route("/api")
@login_required
def api():
    res = Product.query.order_by(Product.id.desc())
    list_drug =[r.as_dict() for r in res]

    return list_drug
@app.route("/searchproduct",methods=['POST'])
@login_required
def searchproduct():
    found = None

    if request.method=='POST':
        product = request.form.get("searchProduct")
        search = "%{}%".format(product)
        found = Product.query.filter(Product.title.like(search)).all()
           
    return render_template("showproduct.html",
                                title="ค้นหาสินค้า",
                                allproducts=found)  

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

@app.route("/api_patient")
@login_required
def api_patient():
    patients = Patient.query.filter_by(pharmacist_id=current_user.id)
    patients_api = [r.as_dict() for r in patients]
    return patients_api