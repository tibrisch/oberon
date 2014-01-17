#!/usr/bin/env python

import sys
import cgi
from miranda import upnp, msearch, main, host

def X_NDS_CreateRecordSchedule(hp, index=0, eventID=17950140):  
    elements =  '\n<srs xmlns="urn:schemas-upnp-org:av:srs" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation=" urn:schemas-upnp-org:av:srs http://www.upnp.org/schemas/av/srs.xsd">\n'\
                '<item id="">\n'\
                '<class>OBJECT.RECORDSCHEDULE.DIRECT.PROGRAMCODE</class>\n'\
                '<scheduledProgramCode type="nds.com_URI">cid://programid://%d~programid://%d</scheduledProgramCode>\n'\
                '</item>\n'\
                '</srs>' % (eventID,eventID)
 
    #host send 0 MediaServer ScheduledRecording X_NDS_CreateRecordSchedule
    host(6, ['host', 'send', str(index), 'MediaServer', 'ScheduledRecording', 'X_NDS_CreateRecordSchedule'] , hp, {'Elements': (cgi.escape(elements), 'string')}) 
    
conn = upnp()
#msearch(0,0,conn,showUniq=True)
msearch(3,['msearch','uuid','444D5376-3247-4D65-6469-001cc3078df7'],conn,showUniq=True)

# populate all the host info, for every upnp device on the network
for index in conn.ENUM_HOSTS:
    hostInfo = conn.ENUM_HOSTS[index]
    if hostInfo['dataComplete'] == False:
        xmlHeaders, xmlData = conn.getXML(hostInfo['xmlFile'])
        conn.getHostInfo(xmlData,xmlHeaders,index)

for i in conn.ENUM_HOSTS:
    for j in conn.ENUM_HOSTS[i]['deviceList']:
        try:
            print "\n[%d]\ndeviceList: %s\nUDN: %s\nfrendlyName: %s" % (i,j,conn.ENUM_HOSTS[i]['deviceList'][j]['UDN'], conn.ENUM_HOSTS[i]['deviceList'][j]['friendlyName'])
        except:
            print "\n[%d]\ndeviceList: %s\nUDN: %s\nfrendlyName: UNKNOWN" % (i,j,conn.ENUM_HOSTS[i]['deviceList'][j]['UDN'])
print

X_NDS_CreateRecordSchedule(conn)

try:
    main(len(sys.argv),sys.argv)
except Exception, e:
    print 'Caught main exception:',e
    sys.exit(1)
