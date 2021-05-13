import json
import urllib.request
import requests
import os
from datetime import datetime
from pandas import json_normalize
import traceback
import app

class VaccineSlot:

    def __init__(self,data):
        '''
        :param data: ["by_district", "district_id", "pin", "min_age"]:
        '''
        self.data = data
        if data["by_district"] == 1:
            self.dist_id = data["district_id"]

    @staticmethod
    def collect_data(json_data, by_district):
        if by_district == 1:
            fname = ""
            words  = json_data["centers"][0]["state_name"].split(" ")
            for word in words:
                fname += word
            fname+="_"
            words = json_data["centers"][0]["district_name"].split(" ")
            for word in words:
                fname += word
            file_name = "response_data/district/" + str(fname) + ".csv"
        else:
            fname = json_data["centers"][0]["pincode"]
            file_name = "response_data/pin/" + str(fname) + ".csv"
        if not os.path.exists(file_name):
            header = True
        else:
            header = False
        df = json_normalize(json_data["centers"])
        df["timestamp"] = str(datetime.now())
        df.to_csv("temp.csv", header=header)

        command = "cat temp.csv >> " + file_name
        os.system(command)
        #print(f"{fname} - data added")

    def get_available_slots(self):
        today = datetime.today().date()
        day = str(today.day)
        month = str(today.month)
        year = str(today.year)
        day = day if len(day) == 2 else "0"+day
        month = month if len(day) == 2 else "0"+month

        date = day + "-" + month + "-" + year
        if self.data["by_district"] == 1:
            self.url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={self.dist_id}&date={date}"
        else:
            pin = self.data["pin"]
            self.url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}"

        proxies = {
         "http": "http://14.140.131.82:3128",
         "https": "http://14.140.131.82:3128"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
        available = {}
        district_name = ""

        #resp = eval(requests.get(self.url, proxies=urllib.request.getproxies()).text)
        #resp = eval(urllib.request.urlopen(self.url).read().decode('utf-8'))
        try:
            resp = requests.get(self.url, headers=headers).content
            #print("responce:",resp)
            resp = eval(resp.decode('utf-8'))
            all_centers = resp['centers']

            if len(all_centers) > 0:
                VaccineSlot.collect_data(resp,self.data["by_district"])
                district_name =  resp["centers"][0]["district_name"]
            min_age = self.data['min_age']
            #print("age=",min_age)

            for each in all_centers:
                center_name = each["name"].strip()
                if each['sessions']:
                    for sess in each['sessions']:
                        #print(sess)
                        if sess['min_age_limit'] == min_age and sess["available_capacity"] >= 2:
                            data = {"available_capacity": sess["available_capacity"]
                                , "date": sess["date"]}
                            if center_name not in available:
                                available[center_name] = [data]
                            else:
                                available[center_name].append(data)
                            #print("available!")
        except Exception as e:
            traceback.print_exc()
            return [e,"error"]


        return [available,district_name]


