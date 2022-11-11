import win32evtlog # requires pywin32 pre-installed

server = 'localhost' # name of the target computer to get event logs
logtype = 'Security' # 'Application' # 'Security'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)
count = 0 

f = open("C://temp/evtlog.txt", "w")

while count<3:
    events = win32evtlog.ReadEventLog(hand, flags,0)
    if events:
        for event in events:
            f.write ("Record Number: %s\n" % str(event.RecordNumber))
            f.write ("Event Category: %s\n" % str(event.EventCategory))
            f.write ("Time Generated: %s\n" % str(event.TimeGenerated))
            f.write ("Source Name: %s\n" % str(event.SourceName))
            f.write ("Event ID: %s\n" % str(event.EventID))
            f.write ("Event Type: %s\n" % str(event.EventType))
            data = event.StringInserts
            f.write("------------------------------\n")
            if data:
                f.write ("Event Data:")
                for msg in data:
                    f.write (msg)
            f.write ("\n=============================================\n")
    count += 1