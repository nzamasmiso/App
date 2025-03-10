
#! /usr/bin/env python3
from wtforms import Form,StringField,PasswordField,validators,SubmitField,TextAreaField,RadioField
#from wtforms.sqlalchemy import QuerySelectField
class RegistrationForm(Form):
	name=StringField("Name",[validators.DataRequired()])
#	surname=StringField("Surname",[validators.DataRequired()])
	id=StringField("ID",[validators.DataRequired(message="Required")])
	email=StringField("Email",[validators.DataRequired(message="Required"),validators.email()])
	password=PasswordField("Password",[validators.DataRequired(message="Required"),validators.Length(min=4)])
	confirm_password=PasswordField("Confirm Password",[validators.DataRequired(message="Required"),validators.EqualTo("password",message="Passwords do not match")])
class ComplaintForm(Form):
	category=StringField("Category",[validators.DataRequired(message="Required")])
class D(RegistrationForm):
	category=StringField("Category",[validators.DataRequired(message="Required")])
class SA(RegistrationForm):
	surname=StringField("Surname",[validators.DataRequired(message="Required")])

class StudentComplaint(Form):
	sid=StringField("Student ID",[validators.DataRequired()])
	deptcode=StringField("Department Code",[validators.DataRequired()])
	description=TextAreaField("Description",[validators.DataRequired()])
	complaint=TextAreaField("Complaint",[validators.DataRequired()])

class LoginForm(Form):
	title=RadioField('',choices=[('student', 'Student'),('admin','Admin'),('department','Department')])
	email=StringField("Email",[validators.DataRequired()])
	password=StringField("Password",[validators.DataRequired()])
