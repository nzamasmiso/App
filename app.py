#! /usr/bin env python3
from flask import Flask, render_template,jsonify,request,flash,redirect,url_for
from werkzeug.security import generate_password_hash
#from sqlalchemy.exc import IntergrityError
from models import *
from forms import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

###############################################################################################################################

app=Flask(__name__)
app.config['SECRET_KEY']='mysecret'
engine=create_engine('sqlite:///example.db')
Session=sessionmaker(bind=engine)

################################################################################################################################

@app.route('/')
def home():
	return render_template('index.html')

#################################################################################################################################

@app.route('/Login',methods=['GET','POST'])
def login():
	session=Session()
	form=LoginForm()
	if request.method=='GET':
		return render_template('Login.html',form=form)
	elif request.method=='POST':
		if form.title.data=='student':
			em=session.query(Student).filter_by(_email=form.email.data).first()
			pas=session.query(Student).filter_by(_password=generate_password_hash(form.password.data)).first()
			if em and pas:
				return redirect(url_for('Dashboard'))
			else:
				message="Incorrect credintials"
				return render_template('Login.html',form=form)
		elif form.title.data=='admin':
			em=session.query(Admin).filter_by(_email=form.email.data).first()
			pas=session.query(Admin).filter_by(_password=generate_password_hash(form.password.data)).first()
			if em or pas:
				return render_template('Dashboard.html')
			else:
				message="Incorrect credintials"
				return render_template('Login.html',form=form)
		elif form.title.data=="department":
			em=session.query(Department).filter_by(_email=form.email.data).first()
			pas=session.query(Department).filter_by(_password=generate_password_hash(form.password.data)).first()
			if em or pas:
				return render_template('Dashboard.html')
			else:
				message="Incorrect credintials"
				return render_template('Login.html',form=form,message=message)
#		else:
#			message="Incorrect credintials"
#			return render_template('Login.html',form=form,message=message)


	#	if title=='student':

	#	elif title=='admin':

	#	elif title=='department':

###################################################################################################################################

@app.route('/Register',methods=['GET','POST'])
def Register():
	session=Session()
	form=SA(request.form)
	if request.method=='GET':
		return render_template('Register.html',form=form)
	if request.method=='POST' and form.validate():
		id=session.query(Student).filter_by(_id=form.id.data).first()
		email=session.query(Student).filter_by(_email=form.email.data).first()
		if id or email:
			message="Email or ID already exists"
			return render_template('Register.html',form=form,message=message)
		if form.password.data!=form.confirm_password.data:
			message="Passwords do not match"
			return render_template('Register.html',form=form,message=message)
		else:
			student=Student(name=form.name.data,surname=form.surname.data,id=form.id.data,email=form.email.data,password=generate_password_hash(form.password.data))
			session.add(student)
			session.commit()
			return redirect(url_for('login'))
	else:
		return render_template('Register.html',form=form)
######################################################################################################################################

@app.route('/Dashboard',methods=['GET'])
def Dashboard():
	session=Session()
	if request.method=='GET':
		students=session.query(StudentComplaint).all()
		output=[]
		for student in students:
			###
		return  render_template('Dashboard.html',output=students)

#######################################################################################################################################

@app.route('/Admin',methods=['GET','POST'])
def Admin_Reg():
	session=Session()
	form=SA(request.form)
	if request.method=='GET':
		return render_template('Admin.html',form=form)
	elif request.method=='POST' and form.validate():
		id=session.query(Admin).filter_by(_id=form.id.data).first()
		email=session.query(Admin).filter_by(_email=form.email.data).first()
		if id or email:
			message="Email or ID already exist"
			return render_template('Admin.html',form=form,message=message)
		if form.password.data!=form.confirm_password.data:
			message='Password do not match'
			return render_template('Admin.html',form=form,message=message)
		else:
			admin=Admin(name=form.name.data,surname=form.surname.data,id=form.id.data,email=form.email.data,password=generate_password_hash(form.password.data))
			session.add(admin)
			session.commit()
			flash('Registration Successfull','success')
			return redirect(url_for('Dashboard'))
				#print(f('Error : {e}')
				#return render_template('Admin.html',form=form)
	else:
		return render_template('Admin.html',form=form)
##########################################################################################################################################		

@app.route('/Complaints',methods=['GET','POST'])
def Complaints():
	session=Session()
	form=ComplaintForm(request.form)
	if request.method=='GET':
		return render_template('complaints.html',form=form)
	if request.method=='POST' and form.validate():
		category=session.query(Category).filter_by(_id=form.id.data).first()
		if category:
			message="Category already exist"
			return render_template('complaints.html',form=form,message=message)
		else:
			message="Category successfully added"
			complaint=Complaint(category=form.category.data)
			session.add(complaint)
			session.commit()
			return render_template('complaints.html',form=form,message=message)

############################################################################################################################################

@app.route('/Department',methods=['GET','POST'])
def department():
	session=Session()
	form=D(request.form)
	if request.method=='GET':
		return render_template('Departments.html',form=form)
	if request.method=='POST' and form.validate():
		id==session.query(Department).filter_by(_id=form.id.data).first()
		email=session.query(Department).filter_by(_email=form.email.data).first()
		
		if id or email:
			message="Email or ID already exist"
			return render_template('Departments.html',form=form,message=message)
		if form.password.data!=form.confirm_password.data:
			message="Passwords do not match"
			return render_template('Departments.html',form=form,message=message)
		else:	
			category=session.query(Category).join(Department).filter(Department._id==form.id.data).first()
			if category:
				department=Department(name=form.name.data,id=form.id.data,category=category,email=form.email.data,password=generate_password_hash(form.password.data))
				session.add(department)
				session.commit()
				return render_template('Departments.html',form=form)
			else:
				message="Invalid Category"
				return render_template('Departments.html',form=form)
#############################################################################################################################################

@app.route('/Students_Complaints',methods=['GET','POST'])
def StudentComplaints():
	session=Session()
	form=StudentComplaint(request.form)
	if request.method=='GET':
		return render_template('Students_Complaints.html',form=form)	
	if request.method=='POST' and form.validate():
		category=session.query(Category).join(Department).filter(Department._id==form.id.data).first()
		if category:
			studentcomplaint=StudentComplain(sid=form.sid.data,deptcode=form.deptcode.data,category=category,description=form.description.data,complain=form.complaint.data)
			session.add(studentcomplaint)
			session.commit()
			return render_template('Dashboard.html')
		else:
			message="Invalid Category"
			return render_template('Students_Complaints.html',form=form,message=message)

if __name__=='__main__':
	app.run(debug=True)

