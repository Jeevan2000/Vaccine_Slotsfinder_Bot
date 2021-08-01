from django.shortcuts import render
import requests
import time
from datetime import date
import os
# Create your views here.

def home(request):
    dist=363
    today = date.today()
    today_date=today.strftime('"%d-%m-%Y"')
    #print(today_date)



    #telegram api to send meassage 'https://api.telegram.org/bot1875712191:AAG5j_7H93w1zLM4PJ8GOzETQue1DK-8aj8/sendMessage?chat_id=-1001506215395&text='
    grpid="free_vaccine_slots_under18_bot"
    telegram_url=os.environ['URL']


    #API url to fetch the data 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(dist,today_date)

    header = {
        os.environ['header']
    }

    # function to check if there are any available slots
    def checkAvailable():
        counter = 0
        result = requests.get(URL, headers=header)
        response_json = result.json()
        data = response_json['sessions']
        #flag=0
        for each in data:
            # checking for each type fee_type and age_limit
            if (each["available_capacity"] > 0) & (each["min_age_limit"] == 18) & (each["fee_type"]=="Free"):
                counter += 1
                s1="Pin Code:  {0}\n\nPune\n\nCenter Name: {1}  \n\nVaccine Name: {2} \nFee: Free\nAge Group: {3}\n\nDose 1 Avaiable Capcity: {4}\nDose 2 Avaiable Capcity: {5}".format(each["pincode"],
                                                                                                                                  each["name"],
                                                                                                                                  each["vaccine"],
                                                                                                                                  each["min_age_limit"],
                                                                                                                                 each["available_capacity_dose1"],
                                                                                                                                 each["available_capacity_dose2"])
            #print(s1)
            
                send_to_tele(s1)
            
            if (each["available_capacity"] > 0) & (each["min_age_limit"] == 18) & (each["fee_type"]=="Paid"):
                counter += 1
                age=str(each["min_age_limit"])+"+"
                s1="Pin Code: {0}\n\nPune\n\nCenter Name: {1}\n\nVaccine Name:   {2}   \nFee: {3}\nAge Group: {4}\n\nDose 1 Avaiable Capcity: {5}\nDose 2 Avaiable Capcity: {6}".format(each["pincode"],
                each["name"],(each["vaccine"]),each["fee"],age,each["available_capacity_dose1"],each["available_capacity_dose2"])
            #print(s1)
                send_to_tele(s1)
            
       
        # Below code is for age limit 45 and above 
        '''    
        if (each["available_capacity"] > 0) & (each["min_age_limit"] == 45) & (each["fee_type"]=="Free"):
            counter += 1
            s1="Pin Code:  {0}\n\nPune\n\nCenter Name: {1}  \n\nVaccine Name: {2} \nFee: Free\nAge Group: {3}\n\nDose 1 Avaiable Capcity: {4}\nDose 2 Avaiable Capcity: {5}".format(each["pincode"],
                                                                                                                                  each["name"],
                                                                                                                                  each["vaccine"],
                                                                                                                                  each["min_age_limit"],
                                                                                                                                 each["available_capacity_dose1"],
                                                                                                                                 each["available_capacity_dose2"])
            print(s1)
            
            send_to_tele(s1)
            flag=1
        if (each["available_capacity"] > 0) & (each["min_age_limit"] == 45) & (each["fee_type"]=="Paid"):
            counter += 1
            age=str(each["min_age_limit"])+"+"
            s1="Pin Code: {0}\n\nPune\n\nCenter Name: {1}\n\nVaccine Name:   {2}  \nFee: {3}\nAge Group: {4}\n\nDose 1 Avaiable Capcity: {5}\nDose 2 Avaiable Capcity: {6}".format(each["pincode"],
            each["name"],(each["vaccine"]),each["fee"],age,each["available_capacity_dose1"],each["available_capacity_dose2"])
            print(s1)
            send_to_tele(s1)
            flag=1
       '''
       
        if(counter == 0):
            print("No Available Slots")
            return False

    def send_to_tele(s1):
        final=telegram_url+s1
        requests.get(final) #sending message to telegram using url
    
    checkAvailable()
    #    time.sleep(600)

    

    return render(request,'home.html')
