import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Backend Final Project-credential.json', scope)
client = gspread.authorize(creds)

sheet = client.open('I-House Mastersheet').get_worksheet(0)

allData = sheet.get_all_records()
print(allData)