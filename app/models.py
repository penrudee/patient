from app import db ,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Pharmacist(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120),index=True, unique=True)
    create_time = db.Column(db.DateTime)
    password_hash = db.Column(db.String(128))
    patients = db.relationship('Patient',backref='doctor',lazy='dynamic')
    paids = db.relationship('Pay',backref='doctor',lazy='dynamic')
    def __repr__(self):
        return '<Pharmacist {}'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Patient(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(200))
    lastname=db.Column(db.String(200))
    nation_id = db.Column(db.String(200))
    phone_no = db.Column(db.String(200))
    create_time = db.Column(db.DateTime,index=True )
    allergies = db.relationship('Allergy',backref='patientName',lazy='dynamic')
    ccs = db.relationship("Chief_complain",backref='patientName',lazy='dynamic')
    pis = db.relationship("Present_illness",backref="patientName",lazy='dynamic')
    meds = db.relationship("Medicine",backref="patientName",lazy='dynamic')
    pharmacist_id = db.Column(db.Integer,db.ForeignKey('pharmacist.id'))

class Allergy(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    thing=db.Column(db.String(200))
    create_time = db.Column(db.DateTime,index=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'))

class Chief_complain(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    cc = db.Column(db.Text)
    create_time=db.Column(db.DateTime,index=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'))

class Present_illness(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    pi = db.Column(db.Text)
    create_time =db.Column(db.DateTime,index=True)
    patient_id =db.Column(db.Integer,db.ForeignKey('patient.id'))

class Medicine(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    med = db.Column(db.Text)
    create_time =db.Column(db.DateTime,index=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'))

class Pay(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    create_time = db.Column(db.DateTime,index=True)
    amount = db.Column(db.String(200))
    paid_time = db.Column(db.DateTime)
    pharmacist_id = db.Column(db.Integer,db.ForeignKey('pharmacist.id'))


@login.user_loader
def load_user(id):
    return Pharmacist.query.get(int(id))