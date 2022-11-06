import win32evtlog # requires pywin32 pre-installed

server = 'localhost' # name of the target computer to get event logs
logtype = 'System' # 'Application' # 'Security'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)
count = 0 

f = open("C://temp/evtlog.txt", "w")

while count<3:
    events = win32evtlog.ReadEventLog(hand, flags,0)
    if events:
        for event in events:
            f.write("Record Number: %s\n" % str(event.RecordNumber))
            print ('Record Number:', event.RecordNumber)
            print ('Event Category:', event.EventCategory)
            print ('Time Generated:', event.TimeGenerated)
            print ('Source Name:', event.SourceName)
            print ('Event ID:', event.EventID)
            print ('Event Type:', event.EventType)
            data = event.StringInserts
            print('------------------------------')
            if data:
                print ('Event Data:')
                for msg in data:
                    print (msg)
            print ("=============================================")
    count += 1