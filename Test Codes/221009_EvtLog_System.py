from http import server
import win32evtlog
import win32con
import unicodedata
import win32evtlogutil

# 이벤트로그 중 System 타입의 이벤트로그를 출력
evtH = win32evtlog.OpenEventLog(None, "System")

Event_Types = {
    1 : "\"Error\"",
    2 : "\"Caution\"",
    4 : "\"Information\"",
    8 : "\"Success Audit\"",
    16 : "\"Failure Audit\"" 
} # Event_Types 출력 칸수 조절

numEvt = win32evtlog.GetNumberOfEventLogRecords(evtH)
print("Total Number of EventLogRecords:", numEvt, "\n")

objects = win32evtlog.ReadEventLog(evtH, win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0, 8192)

# msg = {}

# 각 Property별로 칸 만들기
print("Record# | TimeGenerated | ComputerName | EventType | SourceName\n")

for object in objects:
    print("[" + str(object.RecordNumber) + "]", object.TimeGenerated, object.ComputerName, Event_Types.get(object.EventType, "Unknown"), object.SourceName)
    
    # 각 log별 세부정보를 어떤 방식으로 출력할까? 그냥 보여주기 or 선택한 부분만 보여주기
    # msg.update({object.RecordNumber:str(win32evtlogutil.SafeFormatMessage(object, "Application"))})
    print(str(win32evtlogutil.SafeFormatMessage(object, "System")))
    print("\n")