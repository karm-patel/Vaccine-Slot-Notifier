import pickle
from app import data
import time
from app import mail, Message, app
from datetime import datetime
import traceback
import pytz

# get the standard UTC time
UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')

def format_slots(slots):
    formatted = ""
    for each in slots:
        formatted = "\n" + formatted + each + "\n"
        formatted += str(slots[each]) + "\n"
    return formatted

request_count = 0
request_threshold = 40
while True:
    #n_objects = app.config["USER_OBJECTS"]
    rows = data.query.all()
    objects= pickle.load(open("user_groups", "rb"))
    #objects = pickle.load(open("pickleobjs", "rb"))
    for ind,key in enumerate(objects):
        obj = objects[key]["VaccineSlot_Object"]
        if obj.data["by_district"] == 1:
            district_id, min_age = key.split(":")
            #district = district_id
        else:
            pin, min_age = key.split(":")
        emails = objects[key]["emails"]
        if emails == []:
            continue
        print(f"{ind+1}) {datetime.now(IST)} - {emails}")

        slots,district = obj.get_available_slots()
        if district == "error":
            with app.app_context():
                msg = Message('Exception occured in check.py', sender=app.config['MAIL_USERNAME'],
                              recipients=['karmasmart216@gmail.com',"karmpatel216@gmail.com"])
                msg.body = str(slots)
                mail.send(msg)
            time.sleep(600)
            continue
        #print(slots)
        if slots != {}:
            with app.app_context():
                msg = Message('Vaccine Slot is Available', sender=app.config['MAIL_USERNAME'], bcc=emails)
                n_centers = len(slots)
                if n_centers < 50:
                    formatted_slots = format_slots(slots)
                else:
                    formatted_slots = str(slots)
                #print(formatted_slots)
                if obj.data["by_district"] == 1:
                    msg.body = "Dear user,\nFollowing slots are available in " + str(district) +"\nAge group:"+ str(min_age) +"\n" + str(formatted_slots)
                    print(f"vaccine is available in {district} for age {min_age}+")
                else:
                    msg.body = "Dear user,\nFollowing slots are available in "+ str(pin) +"\nAge group:"+ str(min_age) +"\n" + str(formatted_slots)
                    print(f"vaccine is available in {pin} for age {min_age}+")
                mail.send(msg)

                #print(msg.body)
                print(f"{datetime.now(IST)} - mail sent to-{emails} $$$$$$$$$$$$$$$$$$$$$$$$$")

        time.sleep(4)
        # request_count += (request_count + 1)%request_threshold
        # if request_count == 0:
        #     time.sleep(120)


    print("*********************************")

