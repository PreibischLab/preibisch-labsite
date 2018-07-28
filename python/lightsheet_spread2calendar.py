from bs4 import BeautifulSoup
# Regex:
import re
import pandas as pd
from datetime import date, datetime

script_folder = '/home/ella/preibisch-labsite/python/'
folder = '/home/ella/preibisch-labsite/_external/'

# Set up access to google API:
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
# use creds to create a client to interact with the Google Drive API
# the account for Google Drive API is the lab's google account (so not the same as the first owner as the spreadsheet)
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
         
creds = ServiceAccountCredentials.from_json_keyfile_name("".join([script_folder+'client_secret.json']), scope)
client = gspread.authorize(creds)

# Get each of the worksheets in the spreadsheet (result - list of the worksheets):
sheet = client.open("#LSFM18 program").get_worksheet(0)
# For each worksheet - put the records in a list of hashes:
list_of_hashes = sheet.get_all_records()
# Convert each list of hashes to a dataframe:
all_events = pd.DataFrame(list_of_hashes)

events_str = ""
for i, row in all_events.iterrows():

  events_str = "".join([events_str, '<div class="row">\n'])

  events_str = "".join([events_str, '<div class="col-md-3"><p style="margin:0px;padding:0px;"><b>', row["DAY"], '</b></p></div>\n'])
  events_str = "".join([events_str, '<div class="col-md-3"><p class="text-muted" style="margin:0px;padding:0px;">', row["TIME"],'</p>'])
  events_str = "".join([events_str, '<p class="text-muted" style="margin:0px;padding:0px;"><small>', row["SESSION"],'</small></p></div>\n'])

  events_str = "".join([events_str, '<div class="col-md-6"><p class="text-muted" style="margin:0px;padding:0px;">', row["SPEAKER"], '</p>'])
  events_str = "".join([events_str, '<p class="text-muted" style="margin:0px;padding:0px;"><small>', row["TITLE"], '</small></p></div>\n'])
        
  events_str = "".join([events_str,  '</div>\n'])

  events_str = "".join([events_str, '<hr style="margin:0px;padding:0px;"/>\n\n'])

# Add events to HTML file:

placeholder = 'PROGRAMME_PLACEHOLDER'

f_read = open (script_folder + "lightsheet_workshop_template.txt", "r") 
f_write = open (folder + "lightsheet_workshop.html", "w")

f_r_dump = f_read.read()
f_r_dump = f_r_dump.replace('published: false', 'published: true')
f_r_dump = f_r_dump.replace(placeholder, events_str)

f_write.write(f_r_dump)

f_read.close()
f_write.close()



