import time
import win32file
import win32con
import pywintypes
import winerror
import win32evtlog 
import pandas as pd
import time
import datetime

WATCHED_DIR = "C:\\" # 라이브스캐닝의 대상 디렉터리
    
feature1 = { 'Log Type'       : [],
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
feature2 = { 'Log Type'       : [],
             'Record #'       : [],
             'Event Category' : [],
             'Time Generated' : [],
             'Source Name'    : [],
             'Event ID'       : [],
             'Event Type'     : [],
           }

def clear_feature():
    print("30")
    feature1['Log Type'].clear()
    feature1['Record #'].clear()
    feature1['Event Category'].clear()
    feature1['Time Generated'].clear()
    feature1['Source Name'].clear()
    feature1['Event ID'].clear()
    feature1['Event Type'].clear()
    feature1['Event Data 1'].clear()
    feature1['Event Data 2'].clear()
    feature1['Event Data 3'].clear()
    feature2['Log Type'].clear()
    feature2['Record #'].clear()
    feature2['Event Category'].clear()
    feature2['Time Generated'].clear()
    feature2['Source Name'].clear()
    feature2['Event ID'].clear()
    feature2['Event Type'].clear()

def append_feature1(logtype, event):
    print("27")
    if logtype == "Security":
        print("28")
        feature1['Log Type'].append(logtype)
        feature1['Record #'].append(event.RecordNumber)
        feature1['Event Category'].append(event.EventCategory)
        feature1['Time Generated'].append(event.TimeGenerated)
        feature1['Source Name'].append(event.SourceName)
        feature1['Event ID'].append(event.EventID)
        feature1['Event Type'].append(event.EventType)
        String = event.StringInserts
        feature1['Event Data 1'].append(String[0])
        feature1['Event Data 2'].append(String[1])
        feature1['Event Data 3'].append(String[2])
    else:
        print("29")
        feature1['Log Type'].append(logtype)
        feature1['Record #'].append(event.RecordNumber)
        feature1['Event Category'].append(event.EventCategory)
        feature1['Time Generated'].append(event.TimeGenerated)
        feature1['Source Name'].append(event.SourceName)
        feature1['Event ID'].append(event.EventID)
        feature1['Event Type'].append(event.EventType)
        String = event.StringInserts
        StringList = []
        if String != None:
            StringList = list(String)
        DataLength = len(StringList)
        if DataLength < 3:
            for i in range(0, 3-DataLength):
                StringList.append('None') # 추출한 EventString의 길이가 3보다 작으면 나머지 부분 None으로 채워주기
        feature1['Event Data 1'].append(StringList[0])
        feature1['Event Data 2'].append(StringList[1])
        feature1['Event Data 3'].append(StringList[2])

def append_feature2(logtype, event):
    print("26")
    feature2['Log Type'].append(logtype)
    feature2['Record #'].append(event.RecordNumber)
    feature2['Event Category'].append(event.EventCategory)
    feature2['Time Generated'].append(event.TimeGenerated)
    feature2['Source Name'].append(event.SourceName)
    feature2['Event ID'].append(event.EventID)
    feature2['Event Type'].append(event.EventType)

def create_feature(logtype, button, events):
    if button == True:
        if logtype == "Security":
            print("15")
            if events:
                print("16")
                for event in events:
                    append_feature1(logtype, event)
                print("17")
        elif logtype == "System":
            if events:
                for event in events:
                    append_feature1(logtype, event)
                print("18")    
        elif logtype == "Application":
            if events:
                for event in events:
                    append_feature1(logtype, event)
                print("19")
        else:
            print("Logtype is uncorrectly defined.")
            return
    else:
        if logtype == "Security":
            print("20")
            if events:
                for event in events:
                    print("21")
                    append_feature2(logtype, event)
        elif logtype == "System":
            print("22")
            if events:
                print("23")
                for event in events:
                    append_feature2(logtype, event)
        elif logtype == "Application":
            print("24")
            if events:
                for event in events:
                    print("25")
                    append_feature2(logtype, event)
        else:
            print("Logtype is uncorrectly defined.")
            return

def get_evtx(server, StartTime, button):
    hand_Security    = win32evtlog.OpenEventLog(server, "Security")
    hand_System      = win32evtlog.OpenEventLog(server, "System")
    hand_Application = win32evtlog.OpenEventLog(server, "Application")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
              
    EndRecording_Security    = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
    EndRecording_System      = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
    EndRecording_Application = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜

    count=0
    if button == True:
        while True: 
            print("1")
            count += 1 
            events_Security    = win32evtlog.ReadEventLog(hand_Security, flags,0, 8192)
            events_System      = win32evtlog.ReadEventLog(hand_System, flags,0, 8192)
            events_Application = win32evtlog.ReadEventLog(hand_Application, flags,0, 8192)               
            if events_Security:
                print("2")
                for event in events_Security:
                    if event.TimeGenerated < StartTime:
                        print("3")
                        EndRecording_Security = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        print("4")
                        create_feature("Security", button, events_Security)
            if events_System:
                print("5")
                for event in events_System:
                    if event.TimeGenerated < StartTime:
                        print("6")
                        EndRecording_System = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        print("7")
                        create_feature("System", button, events_System)                        
            if events_Application:
                print("8")
                for event in events_Application:
                    print("9")
                    if event.TimeGenerated < StartTime:
                        print("10")
                        EndRecording_Application = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        print("11")
                        create_feature("Application", button, events_Application)
            print("12")
            DataFrame = pd.DataFrame(feature1)
            DataFrame.to_csv("C:\\temp\\EvtLog_%d.csv" % count)
            print("13")
            clear_feature()
            if EndRecording_Security == EndRecording_System == EndRecording_Application == True:
                print("14")
                break # 모든 로그의 생성시간이 start버튼 누르기 전으로 바꼈으므로 무한반복 while문을 종료
    else:
        while True:
            count += 1
            events_Security    = win32evtlog.ReadEventLog(hand_Security, flags,0)
            events_System      = win32evtlog.ReadEventLog(hand_System, flags,0)
            events_Application = win32evtlog.ReadEventLog(hand_Application, flags,0)
            if events_Security:
                for event in events_Security:
                    if event.TimeGenerated < StartTime:
                        EndRecording_Security = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        create_feature("Security", button, events_Security)
            if events_System:
                for event in events_System:
                    if event.TimeGenerated < StartTime:
                        EndRecording_System = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        create_feature("System", button, events_System)
            if events_Application:
                for event in events_Application:
                    if event.TimeGenerated < StartTime:
                        EndRecording_Application = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        create_feature("Application", button, events_Application)
            DataFrame = pd.DataFrame(feature2)
            DataFrame.to_csv("C:\\temp\\EvtLog_%d.csv" % count)
            clear_feature()
            if EndRecording_Security == EndRecording_System == EndRecording_Application == True:
                break # 모든 로그의 생성시간이 start버튼 누르기 전으로 바꼈으므로 무한반복 while문을 종료

def live_monitoring(): 
    FILE_ACTIONS = {
    1 : "created",
    2 : "deleted",
    3 : "updated",
    4 : "renamed from",
    5 : "renamed to"
    }
    FileData = {
        'Action' : [],
        'File'   : [],
        'Time'   : []
    }
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
    EndTime = datetime.datetime(2022, 12, 2, 1, 30, 00)

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

        # 에러처리            
        bytes = None
        while bytes == None:
            try:
                 bytes = win32file.GetOverlappedResult(hDir, ol, False)
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
    FileData_Dataframe.to_csv("C:\\temp\\LiveScanLog.csv")
      
    button = True #True/False 체크박스 사용자 선택
    get_evtx('localhost', StartTime, button)

if __name__ == "__main__":
    live_monitoring() 