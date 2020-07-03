from flask import Flask,render_template,request,session, flash, escape, request, redirect, url_for
from models import *
from os import urandom
import re
import os
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db.init_app(app)
app.secret_key = urandom(24)

@app.route("/")
def index():
    users = User.query.all()
    if 'user_id' in session :
        for user in users:
            if session['user_id'] == user.user_id :
                return render_template("success.html", message="Hello", name = user.user_name)
    else :
        return render_template("index.html",users=users, message="")


@app.route("/login", methods=["POST"])
def login():
    """ Login to Form """
    if request.method == 'POST' :
        #Get form information.
        user_id = int(request.form.get("user_id"))
        user_password = (request.form.get("user_password"))
        #Make sure the user exits or not
        found_user = User.query.filter_by(user_id = user_id).first()
        if found_user.user_id == user_id :
            session['user_id'] = found_user.user_id
            if found_user.user_password  == user_password :
                session['user_id'] = user_id
                return redirect(url_for('index')) 
        else :
            return render_template("index.html",message="Invalid Credentials")
    return redirect(url_for('index'))
    

@app.route('/signout')
def signout():
    session.pop('user_id')
    return redirect(url_for('index'))


@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == 'POST' :
        "Get the Information"
        try:
            user_id = int(request.form.get("user_id"))
        except ValueError:
            return render_template("register.html", message="Invalid Unique ID.")

        user_id = int(request.form.get("user_id"))
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")
        recurrent = request.form.get("repassword")
                
        #Check if passwords are matched
        if user_password != recurrent :
            return render_template("register.html", user_id = user_id, user_name = user_name, message = "Passwords didn't match!" )
        else :
                found_user = User.query.filter_by(user_id = user_id).first()
                if found_user :
                    if user_id == found_user.user_id :
                        flash("User already Registered")
                        return render_template("index.html" ,message="User already Registered, Please Login")
                else : 
                    # Add the user
                    usr = User(user_id, user_password, user_name)
                    db.session.add(usr)
                    db.session.commit()
                    return render_template("index.html", message = "Registered successfully, Please login")    
    return render_template("register.html", user_id="")


@app.route('/searchPatient', methods = ["POST", "GET"])
def searchPatient():
    if 'user_id' in session :
        if request.method == 'POST' :
            try:
                puid = int(request.form.get("puid"))
            except ValueError:
                return render_template("searchPatient.html", message="Invalid Unique ID.")
            found_patient = Patient.query.filter_by(puid = puid).first()
            if not found_patient :
                return render_template("searchPatient.html", message = "Patient Not found")
            else :
                return render_template("searchPatient.html", message = "Patient Found", pid = found_patient.puid, pname = found_patient.pname)
        else :
            return render_template("searchPatient.html", message ="Please type your search" )
    else :
        return render_template("index.html")


@app.route('/deletePatient', methods = ["POST", "GET"])
def deletePatient():
    if 'user_id' in session :
        if request.method == 'POST' :
            try:
                puid = int(request.form.get("puid"))
            except ValueError:
                return render_template("deletePatient.html", message="Invalid Unique ID.")
            found_patient = Patient.query.filter_by(puid = puid).delete()
            if not found_patient :
                return render_template("deletePatient.html", message = "Patient Not found")
            else :
                db.session.commit()
                return render_template("deletePatient.html", message = "Patient Deleted Successfully")
        else :
            return render_template("deletePatient.html", message ="Please Enter ID to Delete" )
    else :
        return render_template("index.html")




@app.route('/viewPatient')
def viewPatient():
    if 'user_id' in session :
        patients = Patient.query.all()
        return render_template("viewPatient.html", patients = patients)
    else :
        return render_template("index.html")


@app.route('/registerPatient', methods = ["POST", "GET"])
def registerPatient():
    if 'user_id' in session :
        if request.method == 'POST' :

            puid = int(request.form.get("puid"))
            pname = request.form.get("pname")
            page = request.form.get("page")
            pdate = request.form.get("pdate")
            ptypeofbed = request.form.get("ptypeofbed")
            paddress = request.form.get("paddress")
            pstate = request.form.get("pstate")
            pcity = request.form.get("pcity")

            patient = Patient.query.filter_by(puid = puid).first()
            if not patient :
                p = Patient(puid, pname, page, pdate, ptypeofbed, paddress, pstate, pcity)
                db.session.add(p)
                db.session.commit()         
                return render_template("registerPatient.html", message = "Patient Registered Successfully!")
            else :
                if patient.puid == puid :
                    return render_template("registerPatient.html", message="Patient with that ID already Registered !")
                else :
                    return render_template("registerPatient.html")
        else :
            return render_template("registerPatient.html", message = "Fill the Details")
    else :
        return render_template("index.html")

@app.route("/checkUpdatePatient", methods = ["POST","GET"])
def checkUpdatePatient():
    if 'user_id' in session :
        if request.method == 'POST' :
            puid = int(request.form.get("puid"))
            found_patient = Patient.query.filter_by(puid =puid).first()
            if not found_patient :
                return render_template("checkUpdatePatient.html", message = "Enter a Valid Patient ID" )
            else :
                return render_template("masterPatientUpdate.html", message = "Please Update the Details", id = found_patient.puid, name = found_patient.pname, age = found_patient.page, date = found_patient.pdate, typeofbed = found_patient.ptypeofbed, address = found_patient.paddress, state = found_patient.pstate, city = found_patient.pcity  )
        else :
            return render_template("checkUpdatePatient.html", message = "Please enter the patientID to check")
    else :
        return render_template("index.html") 


@app.route("/masterPatientUpdate.html", methods = ["POST","GET"])
def masterPatientUpdate():
    if 'user_id' in session :
        if request.method == 'POST' :
            try:
                puid = int(request.form.get("puid"))
            except ValueError:
                return render_template("masterPatientUpdate.html", message="Invalid Unique ID.")
            founded_patient = Patient.query.filter_by(puid = puid).first()
            founded_patient.pname = request.form.get("pname")
            founded_patient.page = request.form.get("page")
            founded_patient.pdate = request.form.get("pdate")
            founded_patient.ptypeofbed = request.form.get("ptypeofbed")
            founded_patient.paddress = request.form.get("paddress")
            founded_patient.pstate = request.form.get("pstate")
            founded_patient.pcity = request.form.get("pcity")
            db.session.commit()
            return render_template("masterUpdateSuccess.html", message = "Details Updated Successfully")
        else :
            return render_template("masterUpdatePatient", message = "Please Update to confirm")
    else :
        return render_template("index.html")



@app.route("/allocateMedicines", methods = ["POST", "GET"])
def allocateMedicines():
    if 'user_id' in session :
        medicines  = Medicine.query.all()
        allocMedicines = AllocMedicine.query.all()
        if request.method == 'POST' :
            puid = int(request.form.get("puid"))
            found_patient = Patient.query.filter_by(puid = puid).first()       
            if not found_patient :
                return render_template("allocateMedicines.html", message = "Please Enter valid ID", medicines = medicines, allocMedicines = allocMedicines)
            else:
                medicinename = request.form.get("medicinename")
                quantity = int(request.form.get("quantity"))
                found_med = Medicine.query.filter_by(medicinename = medicinename).first()
                total = quantity * found_med.rate
                m = AllocMedicine(medicinename,puid,quantity,total)
                db.session.add(m)
                db.session.commit()
                flash("Medcines Added Successfully")
                return redirect(url_for('allocateMedicines'))
        else :
            flash("Please give a  valid puid")
            return render_template("allocateMedicines.html", message = "Please Add medicines", medicines = medicines, allocMedicines = allocMedicines)
    else :
        return render_template("index.html")


@app.route("/diagnostics", methods = ["POST", "GET"])
def diagnostics():
    if 'user_id' in session :
        diagnostics  = Diagnostic.query.all()
        diagnosticsdone = DiagnosticDone.query.all()
        if request.method == 'POST' :
            puid = int(request.form.get("puid"))
            found_patient = Patient.query.filter_by(puid = puid).first()       
            if not found_patient :
                return render_template("diagnostics.html", message = "Please Enter valid ID", diagnostics = diagnostics, diagnosticsdone = diagnosticsdone)
            else:
                name = request.form.get("name")
                found_d = Diagnostic.query.filter_by(name = name).first()
                rate = found_d.rate
                d = DiagnosticDone(name,puid,rate)
                db.session.add(d)
                db.session.commit()
                flash("Diagonstic Added Successfully")
                return redirect(url_for('diagnostics'))
        else :
            flash("Please give a valid puid")
            return render_template("diagnostics.html", message = "Please Add Diagnostics", diagnostics = diagnostics, diagnosticsdone = diagnosticsdone)
    else :
        return render_template("index.html")



@app.route("/bill", methods = ["POST", "GET"])
def bill():
    if 'user_id' in session :
        if request.method == 'POST' :
            puid = int(request.form.get("puid"))
            found_patient = Patient.query.filter_by(puid = puid).first()       
            if not found_patient :
                return render_template("bill.html", message = "Please Enter valid ID")
            else :
                found_med = AllocMedicine.query.filter_by(patient_id = puid).all()
                bill = 0
                for p in found_med :
                    bill = bill + p.total
                
                found_pat = Patient.query.filter_by(puid = puid).first()
                if found_pat.ptypeofbed.lower() == "single" :
                    bill = bill + 2000
                elif found_pat.ptypeofbed.lower() == "semi" :
                    bill = bill + 4000
                else :
                    bill = bill + 8000
                
                found_d = DiagnosticDone.query.filter_by(patientid = puid).all()
                for d in found_d :
                    bill = bill + d.rate

                return render_template("bill.html", charges = bill)
        return render_template("bill.html", message ="Please enter ID")        
    else :
        return render_template("index.html")