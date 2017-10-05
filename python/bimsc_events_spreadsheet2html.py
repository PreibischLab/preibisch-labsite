from bs4 import BeautifulSoup
# Regex:
import re
import pandas as pd
from datetime import date, datetime

folder = '../_extras/BIMSB_Seminar/'

# Set up access to google API:
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Get each of the worksheets in the spreadsheet (result - list of the worksheets):
sheet = [client.open("BIMSBcalendar").get_worksheet(i) for i in range(3)]
# For each worksheet - put the records in a list of hashes:
list_of_hashes = [sheet[i].get_all_records() for i in range(3)]
# Convert each list of hashes to a dataframe:
all_events = [pd.DataFrame(list_of_hashes[i]) for i in range(3)]
# Concatinate all dataframes together:
all_events = pd.concat(all_events)

# Convert the date column to a date format:
all_events['Date'] = all_events['Date'].apply(pd.to_datetime, dayfirst=True)

# Make individual dataframes for each tab in the HTML:
events_2016 = all_events.loc[all_events['Date'] < datetime(2017, 1, 1)]
events_past2017 = all_events[(all_events['Date'] > datetime(2017, 1, 1)) & (all_events['Date'] < datetime.today().date())]
events_future = (all_events.loc[all_events['Date'] >=  datetime.today().date()]).sort_values(['Date'], ascending=[True])

# Make a list of dataframes - each dataframe belongs to a tab in the HTML:
df_all_events_by_tab = [events_2016, events_past2017, events_future]

# Create the string of HTML for each tab in the HTML:
list_of_strings_4_html = []
for df in df_all_events_by_tab:
    events_str = ""
    for i, row in df.iterrows():
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

placeholders = ['PLACEHOLDER_PAST_2016','PLACEHOLDER_PAST_2017','PLACEHOLDER_FUTURE_EVENTS']

f_read = open ("bimsb_with_placeholder.txt", "r") 
f_write = open (folder + "bimsb_seminar.html", "w")

f_r_dump = f_read.read()
f_r_dump = f_r_dump.replace('published: false', 'published: true')
f_r_dump = f_r_dump.replace(placeholders[0], list_of_strings_4_html[0])
f_r_dump = f_r_dump.replace(placeholders[1], list_of_strings_4_html[1])
f_r_dump = f_r_dump.replace(placeholders[2], list_of_strings_4_html[2])

f_write.write(f_r_dump)

f_read.close()
f_write.close()



