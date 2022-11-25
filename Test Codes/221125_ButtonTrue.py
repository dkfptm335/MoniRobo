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
    
def get_evtx(_server, _StartTime, _PrintEventString):
    server = _server 
    hand_Security    = win32evtlog.OpenEventLog(server, "Security")
    hand_System      = win32evtlog.OpenEventLog(server, "System")
    hand_Application = win32evtlog.OpenEventLog(server, "Application")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

    print("get_evtx_1")

    feature = {'Log Type'       : [],
               'Record #'       : [],
               'Event Category' : [],
               'Time Generated' : [],
               'Source Name'    : [],
               'Event ID'       : [], 
               'Event Type'     : [],
               'Event Data 1'   : [],
               'Event Data 2'   : [],
               'Event Data 3'   : []
              }
              
    print("get_evtx_2")

    EndRecording_Security    = False
    EndRecording_System      = False
    EndRecording_Application = False

    if _PrintEventString == True:
        while True:
            events_Security    = win32evtlog.ReadEventLog(hand_Security, flags,0)
            events_System      = win32evtlog.ReadEventLog(hand_System, flags,0)
            events_Application = win32evtlog.ReadEventLog(hand_Application, flags,0)
        
            print("while_1")
            if events_Security:
                print("record Security")
                for event in events_Security:
                    if event.TimeGenerated < _StartTime:
                        print("Security 시간지남")
                        EndRecording_Security = True
                        break
                    else:
                        print("Security 시간 안지남")
                        feature['Log Type'].append("Security")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        String = event.StringInserts
                        feature['Event Data 1'].append(String[0])
                        feature['Event Data 2'].append(String[1])
                        feature['Event Data 3'].append(String[2])
            print("while_2")
            if events_System:
                print("record System")
                for event in events_System:
                    if event.TimeGenerated < _StartTime:
                        print("System 시간지남")
                        EndRecording_System = True
                        break
                    else:
                        print("System 시간 안지남")
                        feature['Log Type'].append("System")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        String = event.StringInserts
                        StringList = []
                        if String != None:
                            StringList = list(String)
                        DataLength = len(StringList)
                        if DataLength < 3:
                            for i in range(0, 3-DataLength):
                                StringList.append('None')
                        feature['Event Data 1'].append(StringList[0])
                        feature['Event Data 2'].append(StringList[1])
                        feature['Event Data 3'].append(StringList[2])
            print("while_3")
            if events_Application:
                print("record Application")
                for event in events_Application:
                    if event.TimeGenerated < _StartTime:
                        print("Application 시간 지남")
                        EndRecording_Application = True
                        break
                    else:
                        print("Application 시간 안지남")
                        feature['Log Type'].append("Application")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        String = event.StringInserts
                        StringList = []
                        if String != None:
                            StringList = list(String)
                        DataLength = len(StringList)
                        if DataLength < 3:
                            for i in range(0, 3-DataLength):
                                StringList.append('None')
                        feature['Event Data 1'].append(StringList[0])
                        feature['Event Data 2'].append(StringList[1])
                        feature['Event Data 3'].append(StringList[2])
            print("while_4")

            if EndRecording_Security == EndRecording_System == EndRecording_Application == True:
                break
    else:
         while True:
            events_Security    = win32evtlog.ReadEventLog(hand_Security, flags,0)
            events_System      = win32evtlog.ReadEventLog(hand_System, flags,0)
            events_Application = win32evtlog.ReadEventLog(hand_Application, flags,0)
        
            print("while_1")
            if events_Security:
                print("record Security")
                for event in events_Security:
                    if event.TimeGenerated < _StartTime:
                        print("Security 시간지남")
                        EndRecording_Security = True
                        break
                    else:
                        print("Security 시간 안지남")
                        feature['Log Type'].append("Security")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        String = event.StringInserts
                        feature['Event Data 1'].append(String[0])
                        feature['Event Data 2'].append(String[1])
                        feature['Event Data 3'].append(String[2])
            print("while_2")
            if events_System:
                print("record System")
                for event in events_System:
                    if event.TimeGenerated < _StartTime:
                        print("System 시간지남")
                        EndRecording_System = True
                        break
                    else:
                        print("System 시간 안지남")
                        feature['Log Type'].append("System")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        feature['Event Data 1'].append('None')
                        feature['Event Data 2'].append('None')
                        feature['Event Data 3'].append('None')
            print("while_3")
            if events_Application:
                print("record Application")
                for event in events_Application:
                    if event.TimeGenerated < _StartTime:
                        print("Application 시간 지남")
                        EndRecording_Application = True
                        break
                    else:
                        print("Application 시간 안지남")
                        feature['Log Type'].append("Application")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        feature['Event Data 1'].append('None')
                        feature['Event Data 2'].append('None')
                        feature['Event Data 3'].append('None')
            print("while_4")

            if EndRecording_Security == EndRecording_System == EndRecording_Application == True:
                break       

    print("get_evtx_3")
    DataFrame = pd.DataFrame(feature)
    DataFrame.to_csv("C:\\temp\\EvtLog_True.csv")
    print("bye")
    
WATCHED_DIR = "C:\\"

FILE_ACTIONS = {
  1 : "created",
  2 : "deleted",
  3 : "updated",
  4 : "renamed from",
  5 : "renamed to"
}

FileData = {
        'Action' : [],
        'File' : [],
        'Time' : []
    }

def main():
        StartTime = datetime.datetime.now()
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
        EndTime = datetime.datetime(2022, 11, 25, 15, 32, 10)

        while True:
            CurrentTime = datetime.datetime.now()
            if EndTime < CurrentTime:
                break

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
                print(FILE_ACTIONS.get(action, "Unknown"), filename)
                FileData['Action'].append(FILE_ACTIONS.get(action, "Unknown"))
                FileData['File'].append(WATCHED_DIR + filename)
                print(time.ctime())
                FileData['Time'].append(time.ctime())
                print("---")
        
        FileData_Dataframe = pd.DataFrame(FileData)
        FileData_Dataframe.to_csv("C:\\temp\\LiveScanLog_True.csv")
        
        print("hi")
        PrintEventString = True
        print("hi")
        get_evtx('localhost', StartTime, PrintEventString)
        print("hi")

if __name__ == "__main__":
    main()