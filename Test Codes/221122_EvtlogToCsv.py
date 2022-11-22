import win32evtlog # requires pywin32 pre-installed
import pandas as pd

server = 'localhost' # name of the target computer to get event logs
logtype = 'Security' # 'Application' # 'System'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)
count = 0 

data = {'Record #' : [],
        'Event Category' : [],
        'Time Generated' : [],
        'Source Name' : [],
        'Event ID' : [], 
        'Event Type' : [],
        'Event Data' : [],
        }

while count<3:
    events = win32evtlog.ReadEventLog(hand, flags,0)
    if events:
        for event in events:
            data['Record #'].append(event.RecordNumber)
            data['Event Category'].append(event.EventCategory)
            data['Time Generated'].append(event.TimeGenerated)
            data['Source Name'].append(event.SourceName)
            data['Event ID'].append(event.EventID)
            data['Event Type'].append(event.EventType)
            data['Event Data'].append(event.StringInserts)
    count += 1

df = pd.DataFrame(data)
df.to_csv("C://temp/evtlog.csv")