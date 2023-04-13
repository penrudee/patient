from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                            title="Home")

@app.route('/allpatients')
def allpatients():
    return render_template("allpatients.html",
                            title="ผู้ป่วยทั้งหมด")