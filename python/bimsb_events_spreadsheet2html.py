from bs4 import BeautifulSoup
# Regex:
import re
import pandas as pd
from datetime import date, datetime
from collections import OrderedDict

script_folder = '/home/ella/preibisch-labsite/python/'
folder = '/home/ella/preibisch-labsite/_extras/'

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
sheet = [client.open("BIMSB Seminar Series Calendar").get_worksheet(i) for i in range(3)]
# For each worksheet - put the records in a list of hashes:
list_of_hashes = [sheet[i].get_all_records() for i in range(3)]
# Convert each list of hashes to a dataframe:
all_events = [pd.DataFrame(list_of_hashes[i]) for i in range(3)]
# Concatinate all dataframes together:
all_events = pd.concat(all_events, sort=True)

# Convert the date column to a date format:
all_events['Date'] = all_events['Date'].apply(pd.to_datetime, dayfirst=True)

# Make individual dataframes for each tab in the HTML:
events = orderedDict([
    ("events_2016", all_events.loc[all_events['Date'] < datetime(2017, 1, 1)].sort_values(['Date'], ascending=[True])),
    ("events_2017",all_events[(all_events['Date'] < datetime(2018, 1, 1)) & (all_events['Date'] >= datetime(2017, 1, 1))].sort_values(['Date'], ascending=[True])),
    ("events_2018",all_events[(all_events['Date'] < datetime(2019, 1, 1)) & (all_events['Date'] >= datetime(2018, 1, 1))].sort_values(['Date'], ascending=[True])),
    ("events_past2019",all_events[(all_events['Date'] > datetime(2019, 1, 1)) & (all_events['Date'] < pd.Timestamp(datetime.today().date()))].sort_values(['Date'], ascending=[True])),
    ("events_future",(all_events.loc[all_events['Date'] >=  pd.Timestamp(datetime.today().date())]).sort_values(['Date'], ascending=[True]))
    ])

# Create the string of HTML for each tab in the HTML:
list_of_strings_4_html = []
for df in df_all_events_by_tab:
for key,value in events.items():
    events_str = ""
    # each value of "event" orderedDict is a df:
    for i, row in value.iterrows():
        if row['Publish?']=='V':
            events_str = "".join([events_str, '<div class="row">\n'])
            #events_2_paste = "".join([events_2_paste, '<div class="col-md-1"><p>', 
            #                          row["Date"], '<br/><small>', row["Time"], '</small></p></div>\n'])
            if row['Date'] > datetime(2018, 1, 1):
                events_str = "".join([events_str, '<div class="col-md-1"><p>', 
                          row["Date"].strftime('%d %b %Y'), '<br/><small>', row["Time"], '</small></p></div>\n']) 
            else:
                events_str = "".join([events_str, '<div class="col-md-1"><p>', 
                          row["Date"].strftime('%d %b'), '<br/><small>', row["Time"], '</small></p></div>\n']) 


            events_str = "".join([events_str, '<div class="col-md-5">\n'])
            events_str = "".join([events_str, '<p><a href=', row["Link"] ,' target="_blank"><b>', row["Speaker"], '</b></a>, ', 
                     row["Institute"], '<br/><small>Host: ', row["Host"], ', Location: ', row["Location"], '</small></p>\n'])
            events_str = "".join([events_str,  '</div>\n'])
            events_str = "".join([events_str, '<div class="col-md-6">\n'])
            events_str = "".join([events_str, '<p>', row["Talk Title"], '</p>\n'])
            events_str = "".join([events_str, '</div>\n'])
            events_str = "".join([events_str, '</div>\n'])
            events_str = "".join([events_str, '<hr/><br/>\n\n'])
    list_of_strings_4_html.append(events_str)

# Add events to HTML file:

placeholders = [f'PLACEHOLDER_{key[6:].upper}' for key in events]

f_read = open (script_folder + "bimsb_with_placeholder.txt", "r") 
f_write = open (folder + "bimsb_seminar.html", "w")

f_r_dump = f_read.read()
f_r_dump = f_r_dump.replace('published: false', 'published: true')
for i in range(len(placeholders)):
    f_r_dump = f_r_dump.replace(placeholders[i], list_of_strings_4_html[i])

f_write.write(f_r_dump)

f_read.close()
f_write.close()



