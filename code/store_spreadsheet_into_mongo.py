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


def meal_bool_transform(value):
    if value:
        meal_dict = {}
        value = value[1:-1]

        menu_items = value.split(', ')
        for item in menu_items:
            dict_components = item.split('=')
            meal_dict[dict_components[0]] = (dict_components[1]=='true')
        return meal_dict
    else:
        return value



for record in allData:
        
    # remove key and value with '.' and create a new key without '.' with the same value
    key_with_dot = {}
    for key, value in record.items():        
        if "." in key:
            key_with_dot[key] = value

            
    for key, value in key_with_dot.items():
        del record[key]
        new_key = key.replace(".", "")
        if ("Lunch" in key) or ("Dinner" in key):
            new_value = meal_bool_transform(value)
        else:
            new_value = value 
        record[new_key] = new_value 
    
    record["is_completed"] = False
    mycol.insert_one(record)






