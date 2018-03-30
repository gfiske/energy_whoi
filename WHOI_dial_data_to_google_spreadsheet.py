#!/usr/bin/python
#Greg Fiske
#WHOI_dial_data_to_google_spreadsheet.py
#Sept 2016

# import modules
try:
    import urllib, datetime
    from xml.etree import ElementTree as ET    
    import sys, time
    import psycopg2
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


#get yesterday's usage for this time for each building
try:
    #connect
    db = psycopg2.connect(host='10.142.0.2', database='whoibuildingdb', user='whoibuildingdb_readonly', password='energyWHOI')
    cursor = db.cursor()
    #do query on frame table
    myq = "select ts1, (bell * 0.00000027778) * 12 as bell, (challenger * 0.00000027778) * 12 as challenger, (fenno * 0.00000027778) * 12 as fenno, (scylla * 0.00000027778) * 12 as scylla from frame where ts1 >= NOW() - '1 day'::INTERVAL ORDER BY ts1 asc limit 1;"
    cursor = db.cursor()
    cursor.execute(myq)
    # Fetch a single row using fetchone() method.
    myq = cursor.fetchone()
    #parse results of query
    ##mytime = str(myq[0])
    bell = str(round(myq[1],2))
    challenger = str(round(myq[2],2))
    fenno = str(round(myq[3],2))
    scylla = str(round(myq[4],2))
    db.close()
except:
    bell = str(0)
    challenger = str(0)
    fenno = str(0)
    scylla = str(0)



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
worksheet.update_cell(2,7,bell)
worksheet.update_cell(3,7,challenger)
worksheet.update_cell(4,7,fenno)
worksheet.update_cell(5,7,scylla)



