#! /usr/bin/env python3
from sqlalchemy import create_engine,Column,Enum,Integer,String,ForeignKey,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from abc import ABC,abstractmethod
################################################################################################

Base=declarative_base()
engine=create_engine('sqlite:///example.db')

#################################################################################################

class User(Base):
	__abstract__=True

	_name=Column(String,nullable=False)
	_id=Column(String,primary_key=True,nullable=False,unique=True)
	_email=Column(String,unique=True,nullable=False)
	_password=Column(String,nullable=False)	
	def __init__(self,name,id,email,password):
		self._name=name
		self._id=id
		self._email=email
		self._password=password
###################################################################################################

class Student(User):
	__tablename__='student'
	_surname=Column(String,nullable=False)
	def __init__(self,name,surname,id,email,password):
		super().__init__(name,id,email,password)
		self._surname=surname
	def __repr__(self):
		return f"{self._name},{self._surname},{self._id},{self._email},{self._password}"
####################################################################################################

class Admin(User):
	__tablename__='admin'
	_surname=Column(String,nullable=False)
	def __init__(self,name,surname,id,email,password):
		super().__init__(name,id,email,password)
		self._surname=surname

######################################################################################################

class Complaint(Base):
	__tablename__='complaint'
	_ccategory=Column(String,nullable=False,unique=True,primary_key=True)

	def __init__(self,category):
		self._ccategory=category
	def __repr__(self):
		return f"Complaint('{self._ccategory}')"
##################################################################################################

class Department(User):
	__tablename__='department'
	_ccategory=Column(String,ForeignKey('complaint._ccategory'),nullable=False)
	def __init__(self,name,id,category,email,password):
		super().__init__(name,id,email,password)
		self._ccategory=category

	complain=relationship('Complaint',backref='department')
##################################################################################################

#################################################################################################

class StudentComplain(Base):
	__tablename__='student_complain'
	_scid=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
	_s_id=Column(String,ForeignKey('student._id'),nullable=False)
	_deptcode=Column(String,ForeignKey('department._id'))
	_ccategory=Column(String,nullable=False)  #Set category where _deptcode=="Department._dept_code
	_cdescription=Column(String,nullable=False)
	_scomplain=Column(String,nullable=False)
#	_status=Column(Enum(StatusEnum),ForeignKey('statuses.name'),default=StatusEnum.Pending)
	_date=Column(Date,nullable=False)

	def __init__(self,sid,deptcode,category,description,complain):
		self._s_id=sid
		self._deptcode=deptcode
		delf._ccategory=category
		self._cdescription=description
		self._complain=complain
		self._date=setDate()

	def setDate(self):
		return date.today()

	department=relationship("Department",backref='student_complain')
	stud_complain=relationship("Student",backref="student_complain")
#	compplain=relationship("Complaint",backref="student_complain")
#status=relationship('Status',backref='student_complain')
###############################################################################################

################################################################################################

Base.metadata.create_all(engine)

###############################################################################################

