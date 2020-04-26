#!/usr/bin/env python
# coding: utf-8


import pymongo
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Backend Final Project-credential.json', scope)
client = gspread.authorize(creds)

sheet = client.open('I-House Mastersheet').get_worksheet(0)

allData = sheet.get_all_records()


myclient = pymongo.MongoClient("mongodb://mongo:27017/")
mydb = myclient["tasks"]
mycol = mydb["meals"]


for record in allData:
    

    meal_count = 0
    lunch_menu = {}
    dinner_menu = {}
    menu = [lunch_menu, dinner_menu]
    
    # remove key and value with '.' and create a new key without '.' with the same value
    key_with_dot = {}
    for key, value in record.items():        
        if "." in key:
            key_with_dot[key] = value

            
    for key, value in key_with_dot.items():
        del record[key]
        new_key = key.replace(".", "")
        record[new_key] = value           
    
    record["Is_completed"] = False
    mycol.insert_one(record)






