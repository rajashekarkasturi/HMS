import os
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True )
    user_password = db.Column(db.String, nullable = False )
    user_name = db.Column(db.String, nullable = False)

    def __init__(self,user_id, user_password, user_name) :
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password



class Patient(db.Model):
    __tablename__= "patients"
    puid = db.Column(db.Integer, primary_key = True )
    pname = db.Column(db.String, nullable = False )
    page = db.Column(db.Integer, nullable = False )
    pdate = db.Column(db.Date, nullable = False )
    ptypeofbed = db.Column(db.String, nullable = False )
    paddress = db.Column(db.TEXT, nullable = False )
    pstate = db.Column(db.String, nullable = False )
    pcity = db.Column(db.String, nullable = False )

    def __init__(self, puid, pname, page, pdate, ptypeofbed, paddress, pstate, pcity):
        self.puid = puid
        self.pname = pname
        self.page = page
        self.pdate = pdate
        self.ptypeofbed = ptypeofbed
        self.paddress = paddress
        self.pstate = pstate
        self.pcity = pcity

class Medicine(db.Model) :
    __tablename__="medicines"
    medicineid = db.Column(db.Integer, primary_key = True)
    medicinename = db.Column(db.String, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    rate = db.Column(db.Integer, nullable = False) 


class AllocMedicine(db.Model) :
    __tablename__ = "allocatemedicines"
    id = db.Column(db.Integer, primary_key = True)
    medicinename = db.Column(db.String, nullable = False)
    patient_id = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    total = db.Column(db.Integer, nullable = False)

    def __init__(self,medicinename, patient_id, quantity, total) :
        self.medicinename = medicinename
        self.patient_id = patient_id
        self.quantity = quantity
        self.total = total

class Diagnostic(db.Model) :
    __tablename__="diagnostics"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    rate = db.Column(db.Integer, nullable = False) 



class DiagnosticDone(db.Model) :
    __tablename__ = "diagnosticsdone"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    patientid = db.Column(db.Integer, nullable = False)
    rate = db.Column(db.Integer, nullable = False)    

    def __init__(self,name, patientid, rate) :
        self.name = name
        self.patientid = patientid
        self.rate = rate


class checkPassoword() :
    def check(self,password) :
        flag = 0
        while True:   
            if (len(password)<8): 
                flag = -1
                break
            elif not re.search("[a-z]", password): 
                flag = -1
                break
            elif not re.search("[A-Z]", password): 
                flag = -1
                break
            elif not re.search("[0-9]", password): 
                flag = -1
                break
            elif not re.search("[_@$]", password): 
                flag = -1
                break
            else: 
                flag = 0
                return False 

    
        if flag ==-1: 
                return True