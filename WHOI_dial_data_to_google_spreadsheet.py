#!/usr/bin/python
#Greg Fiske
#WHOI_dial_data_to_google_spreadsheet.py
#July 2016

# import modules
try:
    import urllib, datetime
    from xml.etree import ElementTree as ET    
    import psycopg2,sys, time
    import base64
    import ConfigParser
    import gspread
    from oauth2client.client import SignedJwtAssertionCredentials
    import json
except:
    print "Cannot import a module"

###############################################################
config = ConfigParser.RawConfigParser()
config.read('/home/gfiske/Data/python_scripts/gfiske.cfg')
db_user = config.get('section1', 'db_user')
db_passwd = config.get('section1', 'db_passwd')
g_user = config.get('section1', 'g_user')
g_passwd = config.get('section1', 'g_passwd')
db_user = db_user.decode('base64','strict')
db_passwd = db_passwd.strip("'")
email = g_user.decode('base64','strict')
password = g_passwd.decode('base64','strict')[0:15]
chdb_user = config.get('section1', 'chdb_user')
chdb_user = chdb_user.strip("'")
chdb_passwd = config.get('section1', 'chdb_passwd')
chdb_passwd = chdb_passwd.strip("'")
###############################################################

# a function to get the current Grid usage from an eGauge device 
def getData(building):
    eGauge = "eg-" + building + "-00.whoi.net"
    url = "http://" + eGauge + "/cgi-bin/egauge?noteam"
    tree = ET.parse(urllib.urlopen(url)).getroot()
    if len(tree.findall('meter')) == 0:
        currentPower = 0
    for meter in tree.findall( 'meter' ):
        title = meter.attrib['title']
        if title == "Grid":
            currentPower = round(float(meter.findtext("power"))/1000, 2)
    return currentPower

# call the data for each building
buildingList = ['bell', 'challenger', 'clark', 'fenno']
currentUsage = []
for i in buildingList:
    #print str(i) + " current usage is: " + str(getData(i))
    currentUsage.append(getData(i))


#update dials google spreadsheet
json_key = json.load(open('/home/gfiske/Data/python_scripts/raspPi-e0a08639ebab.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
g = gspread.authorize(credentials)
#g = gspread.login(email, password)
worksheet = g.open('WHOI_dials').get_worksheet(0)
worksheet.update_cell(2,1,str(currentUsage[0]))
worksheet.update_cell(2,2,str(currentUsage[1]))
worksheet.update_cell(2,3,str(currentUsage[2]))
worksheet.update_cell(2,4,str(currentUsage[3]))


