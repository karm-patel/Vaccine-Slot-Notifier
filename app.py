from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from slot import VaccineSlot
from datetime import datetime
import pickle
from flask_mail import Mail, Message
import os
import re
import pytz

# get the standard UTC time
UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaccine.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'getvaccineslot@gmail.com'
app.config['MAIL_PASSWORD'] = 'Enter Password here'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

current_path = os.getcwd()
with open(os.path.join(current_path,"slot","district_ids1.json"), "r") as fp:
    district_ids = json.load(fp)

def calculate_objects():
    objects = pickle.load(open("user_groups", "rb"))
    # objects["162:18"]["emails"].remove("karmasmart216@gmail.com")
    user_count = 0
    for obj in objects:
        print(obj)
        print(objects[obj])
        user_count += len(objects[obj]["emails"])
    return user_count

#app.config["USER_OBJECTS"] = calculate_objects()

class data(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.String(20), unique=False, nullable=False)
    pin = db.Column(db.String(20), unique=False, nullable=True)
    district = db.Column(db.String(50), unique=False, nullable=True)
    state = db.Column(db.String(50), unique=False, nullable=True)
    min_age = db.Column(db.String(10), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    timestamp = db.Column(db.String(50), unique=False, nullable=True)


    def __repr__(self):
        return f"Data('{self.email}','{self.min_age}','{self.by}')"

class permanent_data(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.String(20), unique=False, nullable=False)
    pin = db.Column(db.String(20), unique=False, nullable=True)
    district = db.Column(db.String(50), unique=False, nullable=True)
    state = db.Column(db.String(50), unique=False, nullable=True)
    min_age = db.Column(db.String(10), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    timestamp = db.Column(db.String(50), unique=False, nullable=True)


    def __repr__(self):
        return f"Data('{self.email}','{self.min_age}','{self.by}')"

class Feedback(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    feedback = db.Column(db.String(1000), unique=False, nullable=True)

    def __repr__(self):
        return f"Feedback('{self.name}')"
def get_dist_id(state,district):
    with open("district_ids.json", "r") as fp:
        district_ids = json.load(fp)
        dist_id = district_ids[state][district]
    return dist_id

@app.route("/",methods=["POST","GET"])
def home():
    db.create_all()
    states = district_ids.keys()
    active_user_count = len(data.query.all())
    total_user_count = len(permanent_data.query.all())

    #data validation
    if request.method == "POST":
        email = request.form["email"]
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not (re.search(regex, email)):
            flash("Enter Valid Email id","danger")
            return redirect(url_for("home"))

        by = request.form["by"]
        pin = request.form["pin"]
        state = request.form["state"]
        district = request.form["district"]
        if by == "Pincode":
            district = ""
            state = ""
            if len(pin) == 6:
                try:
                    int(pin)
                except:
                    flash("enter valid pincode","danger")
                    return redirect(url_for("home"))
            else:
                flash("enter valid pincode", "danger")
                return redirect(url_for("home"))
        else:
            pin = ""
            if state == "select state":
                flash("select state","danger")
                return redirect(url_for("home"))
            else:
                if district == "select district":
                    flash("select district","danger")
                    return redirect(url_for("home"))

        age = request.form["age"]

        if data.query.filter_by(email=email).first():
            flash("email id already taken","danger")
            return redirect(url_for("home"))
        timestamp =  datetime.now(IST)
        row = data(by=by, pin=pin,district=district,state=state,min_age=age,email=email,timestamp=timestamp)
        row2 = permanent_data(by=by, pin=pin, district=district, state=state, min_age=age, email=email, timestamp=timestamp)
        db.session.add(row)
        db.session.add(row2)
        db.session.commit()

        #make a object
        min_age = 18 if age == "18-44" else 45
        info = {"min_age":min_age}
        if by == "Area":
            info["by_district"] = 1
            info["district_id"] = str(get_dist_id(state,district))
            key = info["district_id"] + ":" + str(min_age)
        else:
            info["by_district"] = 0
            info["pin"] = pin
            key = str(pin) + ":" + str(min_age)
        obj = VaccineSlot(info)

        objects = pickle.load(open(os.path.join(current_path,"user_groups"), "rb"))
        try:
            objects[key]["emails"].append(email)
            print(f"Area already exist")
        except:
            objects[key] = {"VaccineSlot_Object":obj,"emails":[email]}
            print(f"New Area key created")
        pickle.dump(objects, open(os.path.join(current_path,"user_groups"), "wb"))
        #app.config["USER_OBJECTS"] += 1
        flash("you are sucessfully subscribed","success")
        return redirect(url_for("home"))

    return render_template("index.html",states=states,user_count=[active_user_count,total_user_count])
@app.route("/unsubscribe",methods=["POST","GET"])
def unsubscribe():
    if request.method == 'POST':
        email = request.form["email"]
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not (re.search(regex, email)):
            flash("Enter Valid Email id", "danger")
            return redirect(url_for("home"))

        user_record = data.query.filter_by(email=email)
        if user_record.first():
            user =  user_record.first()
            min_age = str(user.min_age)[:2]
            if user.by == "Area":
                district = user.district
                state = user.state
                dist_id = str(get_dist_id(state,district))
                key = dist_id + ":" + min_age
            else:
                pin = str(user.pin)
                key = pin + ":" + min_age


            objects = pickle.load(open(os.path.join(current_path, "user_groups"), "rb"))
            #print(f"before:{objects}")
            try:
                if email in objects[key]["emails"]:
                    objects[key]["emails"].remove(email)
                    if objects[key]["emails"] == []:
                        del objects[key]
                else:
                    flash("email id not found in objects file","danger")
                    return redirect(url_for("home"))


            except Exception:
                flash("Exception occured in removing email","danger")
                return redirect(url_for("home"))

            #print(f"after:{objects}")
            pickle.dump(objects, open(os.path.join(current_path, "user_groups"), "wb"))
            user_record.delete()
            db.session.commit()
            #app.config["USER_OBJECTS"] -= 1
            flash("Unsubscibed!","success")
        else:
            flash("Email id does not exist!","danger")

    return redirect(url_for("home"))


@app.route("/district",methods=["POST","GET"])
def carbrand():

    if request.method == 'POST':
        state = request.form['state']
        #print(state)
        OutputArray = []
        districts = district_ids[state]
        for row in districts:
            outputObj = {
                'state': state,
                'district': row
            }
            OutputArray.append(outputObj)
        #print(OutputArray)
    return jsonify(OutputArray)

@app.route("/feedback",methods=["POST","GET"])
def feedback():
    if request.method == 'POST':
        name = request.form["name"]
        feedback = request.form["feedback"]
        if feedback == "":
            flash("enter feedback","danger")
            return redirect(url_for("home"))
        try:
            feedback = Feedback(name=name,feedback=feedback)
            db.session.add(feedback)
            db.session.commit()
            flash("Your response submitted","success")
        except Exception as e:
            print(e)
            flash("something goes wrong, please try again", "danger")
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True,port=5002)
