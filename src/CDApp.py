#!/usr/bin/env python

import sys
from miranda import upnp, msearch, main

conn = upnp()
msearch(0,0,conn,showUniq=True)

# populate all the host info, for every upnp device on the network
for index in conn.ENUM_HOSTS:
    hostInfo = conn.ENUM_HOSTS[index]
    if hostInfo['dataComplete'] == False:
        xmlHeaders, xmlData = conn.getXML(hostInfo['xmlFile'])
        conn.getHostInfo(xmlData,xmlHeaders,index)

for i in conn.ENUM_HOSTS:
    for j in conn.ENUM_HOSTS[i]['deviceList']:
        print "\n[%d]\ndeviceList: %s\nUDN: %s\nfrendlyName: %s" % (i,j,conn.ENUM_HOSTS[i]['deviceList'][j]['UDN'], conn.ENUM_HOSTS[i]['deviceList'][j]['friendlyName'])
print

try:
    main(len(sys.argv),sys.argv)
except Exception, e:
    print 'Caught main exception:',e
    sys.exit(1)
