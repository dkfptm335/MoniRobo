import os
import time
import win32file
import win32con
import pywintypes
import winerror
import win32process
import win32evtlog # requires pywin32 pre-installed
import pandas as pd
import os.path, time
import datetime

filter_filetype =[".txt", ".exe", "hwp"]

start = 0
end = 0
def filterFile(filename):
    for type in filter_filetype:
        if filename.find(type) != -1:
            return True
    return False
    
def get_evtx(_server, _logtype, _time, show):
    server = _server # name of the target computer to get event logs
    logtype = _logtype # 'Application' # 'System'
    hand = win32evtlog.OpenEventLog(server,logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    count = 0 
    if _logtype == "Security":
        data = {'Record #' : [],
                'Event Category' : [],
                'Time Generated' : [],
                'Source Name' : [],
                'Event ID' : [], 
                'Event Type' : [],
                'Event Data 1' : [],
                'Event Data 2' : [],
                'Event Data 3' : []
                }

        while count < 3:
            events = win32evtlog.ReadEventLog(hand, flags,0)
            if events:
                for event in events:
                    if event.TimeGenerated >= _time:
                        data['Record #'].append(event.RecordNumber)
                        data['Event Category'].append(event.EventCategory)
                        data['Time Generated'].append(event.TimeGenerated)
                        data['Source Name'].append(event.SourceName)
                        data['Event ID'].append(event.EventID)
                        data['Event Type'].append(event.EventType)
                        String = event.StringInserts
                        data['Event Data 1'].append(String[0])
                        data['Event Data 2'].append(String[1])
                        data['Event Data 3'].append(String[2])
                    else:
                        break
            count += 1
        df = pd.DataFrame(data)
        df.to_csv(f"C:\\temp\\{_logtype}_evtlog.csv")
    else:
        if show == False:
            data = {'Record #' : [],
                'Event Category' : [],
                'Time Generated' : [],
                'Source Name' : [],
                'Event ID' : [], 
                'Event Type' : []
                }
            while count < 3:
                events = win32evtlog.ReadEventLog(hand, flags,0)
                if events:
                    for event in events:
                        if event.TimeGenerated >= _time:
                            data['Record #'].append(event.RecordNumber)
                            data['Event Category'].append(event.EventCategory)
                            data['Time Generated'].append(event.TimeGenerated)
                            data['Source Name'].append(event.SourceName)
                            data['Event ID'].append(event.EventID)
                            data['Event Type'].append(event.EventType)
                            
                        else:
                            break
                count += 1

        else:
            data = {'Record #' : [],
                    'Event Category' : [],
                    'Time Generated' : [],
                    'Source Name' : [],
                    'Event ID' : [], 
                    'Event Type' : [],
                    'Event Data 1' : [],
                    'Event Data 2' : [],
                    'Event Data 3' : []
                    }
            while count<3:
                events = win32evtlog.ReadEventLog(hand, flags,0)
                if events:
                    for event in events:
                        if event.TimeGenerated >= _time:
                            data['Record #'].append(event.RecordNumber)
                            data['Event Category'].append(event.EventCategory)
                            data['Time Generated'].append(event.TimeGenerated)
                            data['Source Name'].append(event.SourceName)
                            data['Event ID'].append(event.EventID)
                            data['Event Type'].append(event.EventType)
                            #data['Event Data'].append(event.StringInserts)
                            
                            StringData = event.StringInserts
                            StringList = []
                            if StringData != None:
                                StringList = list(StringData)
                            DataLength = len(StringList)
                            if DataLength < 3:
                                for i in range(0,3-DataLength):
                                    StringList.append('None')
                            data['Event Data 1'].append(StringList[0])
                            data['Event Data 2'].append(StringList[1])
                            data['Event Data 3'].append(StringList[2])

                        else:
                            break
                count += 1

            df = pd.DataFrame(data)
            df.to_csv(f"C:\\temp\\{_logtype}_evtlog.csv")

            
WATCHED_DIR = "C:\\"

FILE_ACTIONS = {
  1 : "created",
  2 : "deleted",
  3 : "updated",
  4 : "renamed from",
  5 : "renamed to"
}

record_data = {
        'Action' : [],
        'File' : [],
        'Time' : []
    }

def main():
        ol = pywintypes.OVERLAPPED()
        buf = win32file.AllocateReadBuffer(1024)
        
        # 디렉토리
        hDir = win32file.CreateFile (
            WATCHED_DIR,                            # fileName
            0x0001, # FILE_LIST_DIRECTORY           # desiredAccess
            win32con.FILE_SHARE_READ |              # shareMode
            win32con.FILE_SHARE_WRITE | 
            win32con.FILE_SHARE_DELETE,
            None,                                   # attributes
            win32con.OPEN_EXISTING,                 # CreationDisposition
            win32con.FILE_FLAG_BACKUP_SEMANTICS |   # flagsAndAttributes
            win32con.FILE_FLAG_OVERLAPPED, # async
            None                                    # hTemplateFile
        )
        count = 0
        while count < 100:
            # read directory changes async
            win32file.ReadDirectoryChangesW(
                hDir,   
                buf,    
                True,   
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME | 
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                ol      
            )
            
            bytes = None

            # 에러처리
            while bytes == None:
                try:
                    bytes = win32file.GetOverlappedResult(
                        hDir,   
                        ol,     
                        False   
                    )

                except pywintypes.error as err:
                    if err.winerror == winerror.ERROR_IO_INCOMPLETE:
                        time.sleep(0.1)
                    else:
                        raise err
            
            result = win32file.FILE_NOTIFY_INFORMATION(buf, bytes)
            
            # 결과출력
            for action, filename in result:
                print("Alert! File Action Alert!!")
                #get_evtx('localhost', 'Application')
                print(FILE_ACTIONS.get(action, "Unknown"), filename)
                record_data['Action'].append(FILE_ACTIONS.get(action, "Unknown"))
                record_data['File'].append(WATCHED_DIR + filename)
                print(time.ctime())
                record_data['Time'].append(time.ctime())
                print("---")
            count = count + 1
            
        end = datetime.datetime.now()
        d = pd.DataFrame(record_data)
        d.to_csv("C:\\temp\\scan_log.csv")
        get_evtx('localhost', 'Security', start, False)
        get_evtx('localhost', "Application", start, False)
        get_evtx('localhost', "System", start, False)

if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
        