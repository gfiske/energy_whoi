#!/usr/bin/python
#WHOI_log_5min_frame_data_to_db.py
#Greg Fiske
#This script collected 5 minute level usage from each WHOI eGauge and inserts values into a postgresql database table
#It also gets the live temperture for Woods Hole from an external spreadsheet
#Dec 2016


# import the modules
try:
    import urllib
    import psycopg2
    from xml.etree import ElementTree as ET    
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import json    
except:
    print "Cannot import a module"


#########################################
#          PULL FROM EGAUGE       #
#########################################

# a function to get aggregated Grid usage from an eGauge device 
def getData(building):
    eGauge = "eg-" + building + "-00.whoi.net"
    url = "http://" + eGauge + "/cgi-bin/egauge-show?m&n=2&s=4&C"
    powerUsed = 0
    try:
        tree = ET.parse(urllib.urlopen(url)).getroot()
        if len(tree.findall('meter')) == 0:
            currentPower = 0
        for c in tree.findall('data'):
            columns = c.attrib['columns']
            columns = int(columns) + 1    
        grid = abs(int(tree[0][columns][0].text))
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
    #########################################
    #               Update db               #
    #########################################
    
    #get temperature data from external spreadsheet
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/root/python_scripts/energy-whoi-74fc1f82a002.json', scope)
    g = gspread.authorize(credentials)      
    worksheet = g.open('Current Conditions').get_worksheet(0)    
    temp = worksheet.acell('B2').value    

    #connect to db
    db = psycopg2.connect("host='localhost' dbname='whoibuildingdb' user='whoi' password='energywhoi'")
    cursor = db.cursor()
    #build query
    myquery = "insert into frame values (DEFAULT, NOW()," + str(temp) + "," + str(Usage[0]) + "," + str(Usage[1]) + "," + str(Usage[3]) + "," + str(Usage[2]) + ");"
    #execute query
    cursor.execute(myquery)
    db.commit()
    #close db connection
    db.close()
    
except:
    print "update database failed"

