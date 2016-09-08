#!/usr/bin/python
#Greg Fiske
#WHOI_dial_data_to_google_spreadsheet.py
#Sept 2016

# import modules
try:
    import urllib, datetime
    from xml.etree import ElementTree as ET    
    import sys, time
    import base64
    import ConfigParser
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import json
except:
    print "Cannot import a module"


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
            currentPower = abs(round(float(meter.findtext("power"))/1000, 2))
    return currentPower

# call the data for each building
buildingList = ['bell', 'challenger', 'clark', 'fenno']
currentUsage = []
for i in buildingList:
    #print str(i) + " current usage is: " + str(getData(i))
    currentUsage.append(getData(i))


#update dials google spreadsheet
#json_key = json.load(open('/root/python_scripts/energy-whoi-74fc1f82a002.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/root/python_scripts/energy-whoi-74fc1f82a002.json', scope)
g = gspread.authorize(credentials)
worksheet = g.open('WHOI_dials').get_worksheet(0)
worksheet.update_cell(2,1,str(currentUsage[0]))
worksheet.update_cell(2,2,str(currentUsage[1]))
worksheet.update_cell(2,3,str(currentUsage[2]))
worksheet.update_cell(2,4,str(currentUsage[3]))


