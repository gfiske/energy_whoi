# import the modules
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import json
except:
    print "Cannot import a module"
    

try:
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/root/python_scripts/energy-whoi-74fc1f82a002.json', scope)
    g = gspread.authorize(credentials)    
    worksheet = g.open('Current Conditions').get_worksheet(0)    
    val = worksheet.acell('B2').value
    print val
except:
    print "Cannot access spreadsheet or some shit..."