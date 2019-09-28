# -*- encoding: utf-8 -*-
"""
Dark Dashboard - coded in Flask
Author: AppSeed.us - App Generator 
"""

# all the imports necessary
from flask import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound, abort

import os
from os.path import join, dirname, realpath
import sys
from werkzeug    import secure_filename

from app  import app

from flask       import url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app         import app, lm, db, bc
from . models    import User, People
from . common    import COMMON, STATUS
from . assets    import *
from . forms     import LoginForm, RegisterForm, AddPeopleForm, PeopleSearchForm
from . process import val, calculate_sum

import os, shutil, re, cgi
        
# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authenticate user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# register user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # define login form here
    form = RegisterForm(request.form)

    msg = None

    # custommize your pate title / description here
    page_title       = 'Register - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, registration page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        name     = request.form.get('name'    , '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:                    
            pw_hash = bc.generate_password_hash(password)

            user = User(username, pw_hash, name, email)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/register.html', 
                                                     form=form,
                                                     msg=msg) )

# authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # define login form here
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # custommize your page title / description here
    page_title = 'Login - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, login page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/login.html', 
                                                     form=form,
                                                     msg=msg) )

# add people
@app.route('/add_people.html', methods=['GET', 'POST'])
def add_people():
    
    # define add people form here
    form = AddPeopleForm()

    msg = None
    
    # custommize your pate title / description here
    page_title       = 'Add People - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, registration page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        name        = request.form.get('name',      '', type=str)
        email       = request.form.get('email',     '', type=str) 
        age         = request.form.get('age'  ,     '', type=int) 
        gender      = request.form.get('gender',    '', type=str)
        photo       = request.files['photo']

        # filter User out of database through username
        people_by_email = People.query.filter_by(email=email).first()
        
        if people_by_email:
            msg = 'Error: People exists!'
            
        else:
            image_url = 'images/'+secure_filename(photo.filename)
            photo.save(join(dirname(realpath(__file__)), "static/"+image_url))
            recognition_data = val(join(dirname(realpath(__file__)), "static/"+image_url))

            people = People(name, email, age, gender, image_url, recognition_data)

            people.save()

            msg = 'People added successfully'     

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/add_people.html', 
                                                     form=form,
                                                     msg=msg) )

# Used only for static export
@app.route('/user.html')
def user():

    # custommize your page title / description here
    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/user.html') )

# Used only for static export
@app.route('/icons.html')
def icons():

    # custommize your page title / description here
    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/icons.html') )

# Used only for static export
@app.route('/tables.html')
def tables():

    # custommize your page title / description here
    page_title = 'Tables - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the tables page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/tables.html') )

# Used only for static export
@app.route('/notifications.html')
def notifications():

    # custommize your page title / description here
    page_title = 'Tables - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the tables page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/notifications.html') )

# Used only for static export
@app.route('/typography.html')
def typography():

    # custommize your page title / description here
    page_title = 'Typography - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the tables page.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/typography.html') )

# Main page (Search) routing
@app.route('/', methods=['GET', 'POST'])
def search():

    # define add people form here
    form = PeopleSearchForm()
    people=[]
    image_url = None
    score = None
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        search_image       = request.files['search_image']
        image_url = 'uploaded_image/'+secure_filename(search_image.filename)
        search_image.save(join(dirname(realpath(__file__)), 'static/'+image_url))

        search_data = val(join(dirname(realpath(__file__)), 'static/'+image_url))
        recognize = 100.0
        for person in People.query.all():
            #print(person)
            distance = calculate_sum(search_data,person.recognition_data)
            print("dis = ", distance, file=sys.stdout)
            if(distance<recognize):
                recognize = distance
                #print(distance, file=sys.stdout)
                if(recognize<0.4):
                    people = [person]
                #break
        #print(People.query.all())
        #single_person = People.query.first()
        #people = [single_person]

        #recognize = calculate_sum(search_data, single_person.recognition_data)

        #print(recognize, file=sys.stdout)

        score = (1- recognize) * 100
    
    else:
        people = People.query.all()
        print(people)
    
    return render_template('layouts/default.html',
                                content=render_template( 'pages/index.html', 
                                form=form,
                                people=people,
                                search_image = image_url,
                                score = score) )

# Generic routing
@app.route('/<path>')
def index(path):

    content = None

    try:

        # try to match the pages defined in -> themes/light-bootstrap/pages/
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path) )
    except:
        abort(404)

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#@app.route('/sitemap.xml')
#def sitemap():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'sitemap.xml')

# ------------------------------------------------------

# error handling
# most common error codes have been added for now
# TO DO:
# they could use some styling so they don't look so ugly

def http_err(err_code):
	
    err_msg = 'Oups !! Some internal error ocurred. Thanks to contact support.'
	
    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:    
        err_msg  = "The URL you were looking for does not seem to exist."
        err_msg += "<br /> Define the new page in /pages"
    
    elif 500 == err_code:    
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg
    
@app.errorhandler(401)
def e401(e):
    return http_err( 401) # "It seems like you are not allowed to access this link."

@app.errorhandler(404)
def e404(e):
    return http_err( 404) # "The URL you were looking for does not seem to exist.<br><br>
	                      # If you have typed the link manually, make sure you've spelled the link right."

@app.errorhandler(500)
def e500(e):
    return http_err( 500) # "Internal error. Contact the manager about this."

@app.errorhandler(403)
def e403(e):
    return http_err( 403 ) # "Forbidden access."

@app.errorhandler(410)
def e410(e):
    return http_err( 410) # "The content you were looking for has been deleted."

	