# -*- encoding: utf-8 -*-
"""
Flask Boilerplate
Author: AppSeed.us - App Generator 
"""

from flask_wtf          import FlaskForm, RecaptchaField
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])
	name        = StringField  (u'Name'      , validators=[DataRequired()])

class AddPeopleForm(FlaskForm):
	name    		= StringField  (u'Name'  		, validators=[DataRequired()])
	email		   	= StringField(u'Email'  		, validators=[DataRequired(), Email()])
	age				= IntegerField(u'Age'			, validators=[DataRequired()])
	gender			= SelectField(u'Gender'      	, validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
	photo			= FileField(u'People photo'		, validators=[FileRequired()])

class PeopleSearchForm(FlaskForm):
	search_image	= FileField(u'Search image'		, validators=[FileRequired()])