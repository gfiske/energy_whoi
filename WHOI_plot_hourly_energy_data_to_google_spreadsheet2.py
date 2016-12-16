#!/usr/bin/python
#Greg Fiske
#This script writes aggregated energy data from WHOI campus buildings to a google spreadsheet hourly for monitoring and plotting
#Sept 2016


# import the modules
try:
    import urllib
    from datetime import datetime
    from pytz import timezone    
    from xml.etree import ElementTree as ET    
    import sys, time
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import json
except:
    print "Cannot import a module"


#########################################
#          PULL FROM EGAUGE       #
#########################################

# a function to get aggregated last hour Grid usage from an eGauge device 
def getData(building):
    eGauge = "eg-" + building + "-00.whoi.net"
    url = "http://" + eGauge + "/cgi-bin/egauge-show?m&n=2&s=59&C"
    powerUsed = 0
    try:
        tree = ET.parse(urllib.urlopen(url)).getroot()
        if len(tree.findall('meter')) == 0:
            currentPower = 0
        for c in tree.findall('data'):
            columns = c.attrib['columns']
            columns = int(columns) + 1    
        grid = round(abs(float(tree[0][columns][0].text) / 3600) / 1000, 2)
        powerUsed = grid
    except:
        pass
    return powerUsed

# call the data for each building
buildingList = ['bell', 'challenger', 'clark', 'fenno']
Usage = []
for i in buildingList:
    #print str(i) + " last hour usage is: " + str(getData(i))
    Usage.append(getData(i))

try:
    #----------------------------
    #enter the data into the google spreadsheet
    #convert to US/Eastern time zone
    now_utc = datetime.now(timezone('UTC'))
    now_eastern = now_utc.astimezone(timezone('US/Eastern'))
    rowToAdd = now_eastern.strftime('%m/%d/%Y'),now_eastern.strftime('%H:%M:%S'),now_eastern.strftime("%Y-%m-%d %H:%M:%S"),str(Usage[0]),str(Usage[1]),str(Usage[2]),str(Usage[3])
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/root/python_scripts/energy-whoi-74fc1f82a002.json', scope)
    g = gspread.authorize(credentials)    
    worksheet = g.open('WHOI_hourly2').get_worksheet(0)
    worksheet.append_row(rowToAdd)
except:
    print "update spreadsheet failed"

