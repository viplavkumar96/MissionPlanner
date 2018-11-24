from flask import Flask, g, render_template, flash, redirect, url_for, abort, session, request, make_response,flash
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import *
import datetime
from geopy.geocoders import Nominatim
#from proto import *
app = Flask(__name__)
app.secret_key = 'DevangIsTheGreatest'



@app.route('/')
def index():
    if session.get("login"):
        return render_template('index.html')
    else:
        print(request.cookies)
        if request.cookies.get('login')=='1':
            session["login"]=True
            session["user_id"] = request.cookies.get('user_id')
            session["username"] = request.cookies.get('username')
            session["email"] = request.cookies.get('email')
            return redirect('/')
        return redirect('/login')





@app.route('/register', methods=["POST","GET"])
def register_page():
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        email=request.form["email"]
        user_register(username,password,email)
        flash("User successfully registered")
        return render_template('login.html')
    else:
        return render_template('register.html')

@app.route('/login', methods=["POST","GET"])
def login_page():
    if request.method=='POST':
        result = user_login(request.form["email"],request.form["password"])
        if result:
            session["login"] = True
            session["user_id"] = result[0]
            session["username"] = result[1]
            session["email"] = result[3]
            resp = make_response(redirect('/'))
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=90)
            resp.set_cookie('user_id', str(result[0]), expires=expire_date)
            resp.set_cookie('username', result[1], expires=expire_date)
            resp.set_cookie('email', result[3], expires=expire_date)
            resp.set_cookie('login','1', expires=expire_date)
            return resp
    return render_template('login.html')

@app.route('/logout')
def logout():
    session["login"] = False
    session["user_id"] = ""
    session["username"] = ""
    session["email"] = ""
    resp = make_response(render_template('login.html'))
    resp.set_cookie('login','0')
    return resp

@app.route('/mission', methods = ["POST","GET"])
def mission():
    if request.method=='POST':
        if session["login"] ==True:
            streetloc=request.form["street"]
            typeofmission=request.form["typeofmission"]
            indoor_outdoor=request.form["indoor_outdoor"]
            minmaj=request.form["minmaj"]
            user_id = session["user_id"]
            nom  = Nominatim()
            n = nom.geocode(streetloc)
            latitude = n.latitude
            longitude = n.longitude
            number_of_drones = drones_query(typeofmission,minmaj)
            #if number_of_drones>0:
            mission_creation(streetloc,typeofmission,indoor_outdoor,minmaj,user_id,latitude,longitude)
            return render_template('index.html')
    else:
        message = "Please Enter Mission Details"
        return render_template('mission.html', mission = mission)




        




if __name__ == '__main__':
    # session["login"] = False
    app.run(debug=True)
