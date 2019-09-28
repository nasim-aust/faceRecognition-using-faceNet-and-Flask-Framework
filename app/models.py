# -*- encoding: utf-8 -*-
"""
Flask Boilerplate
Author: AppSeed.us - App Generator 
"""

from app         import db
from flask_login import UserMixin

from . common    import COMMON, STATUS, DATATYPE

class User(UserMixin, db.Model):

    id          = db.Column(db.Integer,     primary_key=True)
    user        = db.Column(db.String(64),  unique = True)
    email       = db.Column(db.String(120), unique = True)
    name        = db.Column(db.String(500))
    role        = db.Column(db.Integer)
    password    = db.Column(db.String(500))
    password_q  = db.Column(db.Integer)

    def __init__(self, user, password, name, email):
        self.user       = user
        self.password   = password
        self.password_q = DATATYPE.CRYPTED
        self.name       = name
        self.email      = email

        self.group_id = None
        self.role     = None

    def __repr__(self):
        return '<User %r>' % (self.id)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 

class People(db.Model):

    id          = db.Column(db.Integer,     primary_key=True)
    name        = db.Column(db.String(250))
    email       = db.Column(db.String(120))
    age        = db.Column(db.Integer)
    gender        = db.Column(db.Integer)
    image_url    = db.Column(db.String(500))
    recognition_data  = db.Column(db.String(10000))

    def __init__(self, name, email, age, gender, image_url, recognition_data):
        self.name               = name
        self.email              = email
        self.age                = age
        self.gender             = gender
        self.image_url          = image_url
        self.recognition_data   = recognition_data

    def __repr__(self):
        return '<People %r>' % (self.id)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 