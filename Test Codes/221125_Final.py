import os
import time
import win32file
import win32con
import pywintypes
import winerror
import win32process
import win32evtlog 
import pandas as pd
import os.path, time
import datetime
    
def get_evtx(_server, _StartTime, _PrintEventString):
    server = _server 
    hand_Security    = win32evtlog.OpenEventLog(server, "Security")
    hand_System      = win32evtlog.OpenEventLog(server, "System")
    hand_Application = win32evtlog.OpenEventLog(server, "Application")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

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
              
    EndRecording_Security    = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
    EndRecording_System      = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
    EndRecording_Application = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
 
    if _PrintEventString == True:
        while True:
            events_Security    = win32evtlog.ReadEventLog(hand_Security, flags,0)
            events_System      = win32evtlog.ReadEventLog(hand_System, flags,0)
            events_Application = win32evtlog.ReadEventLog(hand_Application, flags,0)
        
            if events_Security:
                for event in events_Security:
                    if event.TimeGenerated < _StartTime:
                        EndRecording_Security = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
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
            if events_System:
                for event in events_System:
                    if event.TimeGenerated < _StartTime:
                        EndRecording_System = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
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
                                StringList.append('None') # 추출한 EventString의 길이가 3보다 작으면 나머지 부분 None으로 채워주기
                        feature['Event Data 1'].append(StringList[0])
                        feature['Event Data 2'].append(StringList[1])
                        feature['Event Data 3'].append(StringList[2])
            if events_Application:
                for event in events_Application:
                    if event.TimeGenerated < _StartTime:
                        EndRecording_Application = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
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
                                StringList.append('None') # 추출한 EventString의 길이가 3보다 작으면 나머지 부분 None으로 채워주기
                        feature['Event Data 1'].append(StringList[0])
                        feature['Event Data 2'].append(StringList[1])
                        feature['Event Data 3'].append(StringList[2])

            if EndRecording_Security == EndRecording_System == EndRecording_Application == True:
                break # 모든 로그의 생성시간이 start버튼 누르기 전으로 바꼈으므로 무한반복 while문을 종료
    else:
         while True:
            events_Security    = win32evtlog.ReadEventLog(hand_Security, flags,0)
            events_System      = win32evtlog.ReadEventLog(hand_System, flags,0)
            events_Application = win32evtlog.ReadEventLog(hand_Application, flags,0)
        
            if events_Security:
                for event in events_Security:
                    if event.TimeGenerated < _StartTime:
                        EndRecording_Security = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
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
            if events_System:
                for event in events_System:
                    if event.TimeGenerated < _StartTime:
                        EndRecording_System = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        feature['Log Type'].append("System")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        feature['Event Data 1'].append('None') # EventString을 출력하지 않기로 했으므로 전부 None으로 채우기
                        feature['Event Data 2'].append('None') # EventString을 출력하지 않기로 했으므로 전부 None으로 채우기
                        feature['Event Data 3'].append('None') # EventString을 출력하지 않기로 했으므로 전부 None으로 채우기
            if events_Application:
                for event in events_Application:
                    if event.TimeGenerated < _StartTime:
                        EndRecording_Application = True # 로그의 생성시간이 start버튼 누른 시간보다 이전이므로 True로 바꾸고 break
                        break
                    else:
                        feature['Log Type'].append("Application")
                        feature['Record #'].append(event.RecordNumber)
                        feature['Event Category'].append(event.EventCategory)
                        feature['Time Generated'].append(event.TimeGenerated)
                        feature['Source Name'].append(event.SourceName)
                        feature['Event ID'].append(event.EventID)
                        feature['Event Type'].append(event.EventType)
                        feature['Event Data 1'].append('None') # EventString을 출력하지 않기로 했으므로 전부 None으로 채우기
                        feature['Event Data 2'].append('None') # EventString을 출력하지 않기로 했으므로 전부 None으로 채우기
                        feature['Event Data 3'].append('None') # EventString을 출력하지 않기로 했으므로 전부 None으로 채우기

            if EndRecording_Security == EndRecording_System == EndRecording_Application == True:
                break # 모든 로그의 생성시간이 start버튼 누르기 전으로 바꼈으므로 무한반복 while문을 종료

    DataFrame = pd.DataFrame(feature)
    DataFrame.to_csv("C:\\temp\\EvtLog.csv")
    
WATCHED_DIR = "C:\\" # 라이브스캐닝의 대상 디렉터리

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

def main(): # main함수 이름 바꾸기
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
        EndTime = datetime.datetime(2022, 11, 25, 17, 43, 00)

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
        FileData_Dataframe.to_csv("C:\\temp\\LiveScanLog.csv")
        
        PrintEventString = True #True/False 체크박스 사용자 선택
        get_evtx('localhost', StartTime, PrintEventString)

if __name__ == "__main__":
    main() 