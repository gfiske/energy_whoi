#WHOI_ServerRoom_basic_read_eGauge.py
#reads energy data from eGauge
#gfiske July 2016

import urllib, datetime
from xml.etree import ElementTree as ET

# Enter eGauge name
eGauge = "eg-clark-00.whoi.net"

# Get XML from eGauge device
#url = "http://" + eGauge + ".egaug.es/cgi-bin/egauge?noteam"
url = "http://" + eGauge + "/cgi-bin/egauge?noteam"

# Parse the results
tree = ET.parse(urllib.urlopen(url)).getroot()
timestamp  = tree.findtext("timestamp")
print
print "Current timestamp is: " + (
    datetime.datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')
)
print
print "Current stats..."
# Get meter level results
for meter in tree.findall( 'meter' ):
    #print meter
    title = meter.attrib['title']
    if title == "Scylla 1 + Scylla 2":
        scylla1 = meter.findtext("power")
        print "scylla1 value: " + scylla1 + " watts"
print


