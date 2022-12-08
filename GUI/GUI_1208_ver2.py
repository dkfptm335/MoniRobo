from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import os
import tkinter
import win32file
import win32con
import string
import sys
import math
from ctypes import windll
from tkinter import ttk
import webbrowser
import tkinter.messagebox
import datetime, time
import winerror
import pywintypes
import win32evtlog  # requires pywin32 pre-installed
import os.path

import pandas as pd
from tkinter import filedialog

from pandastable.core import Table
from threading import Thread

FilePathList = []
FilePath = None
# 여기부터 ButtonTrue.py 코드w
filter_filetype = [".txt", ".exe", "hwp"]

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

def clear_feature():
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
    if logtype == "Security":
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
            if events:
                for event in events:
                    append_feature1(logtype, event)
        elif logtype == "System":
            if events:
                for event in events:
                    append_feature1(logtype, event)  
        elif logtype == "Application":
            if events:
                for event in events:
                    append_feature1(logtype, event)
        else:
            print("Logtype is uncorrectly defined.")
            return
    else:
        if logtype == "Security":
            if events:
                for event in events:
                    append_feature2(logtype, event)
        elif logtype == "System":
            if events:
                for event in events:
                    append_feature2(logtype, event)
        elif logtype == "Application":
            if events:
                for event in events:
                    append_feature2(logtype, event)
        else:
            print("Logtype is uncorrectly defined.")
            return

def get_evtx(server, StartTime, button):
    global WATCHED_DIR
    hand_Security    = win32evtlog.OpenEventLog(server, "Security")
    hand_System      = win32evtlog.OpenEventLog(server, "System")
    hand_Application = win32evtlog.OpenEventLog(server, "Application")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
              
    EndRecording_Security    = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
    EndRecording_System      = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
    EndRecording_Application = False # 추출한 로그의 시간이 start 버튼 누른 시간보다 이전이면 True로 바뀜
    count=0
    while True: 
        count += 1 
        events_Security    = win32evtlog.ReadEventLog(hand_Security, flags,0, 8192)
        events_System      = win32evtlog.ReadEventLog(hand_System, flags,0, 8192)
        events_Application = win32evtlog.ReadEventLog(hand_Application, flags,0, 8192)               
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
        if button==True:
            DataFrame = pd.DataFrame(feature1)
            SavePath=str(WATCHED_DIR+"EvtLog_"+str(count)+".csv")
            DataFrame.to_csv(SavePath)
        elif button==False:
            DataFrame = pd.DataFrame(feature2)
            SavePath=str(WATCHED_DIR+"EvtLog_"+str(count)+".csv")
            DataFrame.to_csv(SavePath)
        clear_feature()
        if EndRecording_Security == EndRecording_System == EndRecording_Application == True:
            break # 모든 로그의 생성시간이 start버튼 누르기 전으로 바꼈으므로 무한반복 while문을 종료

class MyTable(Table):

    def __init__(self, parent=None, **kwargs):
        Table.__init__(self, parent, **kwargs)
        return


def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")

def filterFile(filename):
    for type in filter_filetype:
        if filename.find(type) != -1:
            return True
    return False
 
class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        # self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)
        self.var_6 = tk.StringVar()
        self.var_6.set("Test 1")
        self.cntline=1.0
        # self.var_7 = tk.StringVar()

        # Create widgets :)
        self.setup_widgets()

    def get_FilePath(self):
        global WATCHED_DIR
        if len(FilePathList) == 1 and (FilePathList[0] == 'C:' or FilePathList[0] == 'D:' or FilePathList[0] == "E:"
                                       or FilePathList[0] == "F:" or FilePathList[0] == "G:" or FilePathList[
                                           0] == "H:"):
            WATCHED_DIR = str(FilePathList[0] + '\\')
            return FilePathList[0] + '\\'

        else:
            FilePath = '\\'.join(FilePathList)
            WATCHED_DIR = str(FilePath+'\\')
            return str(WATCHED_DIR)

    def get_drives(self):
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter + ':')
            bitmask >>= 1
        return drives

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def get_dirsize(self, start_path='.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size

    # Layout for Tab2(Shows which Drive or file that you can connect)
    def print_FileList(self):
        global FilePathList
        try:
            self.var_6.set("")
            self.explorer.config(state="normal")
            self.var_6.set(self.var_6.get() + "Path: " + self.get_FilePath() + "\n")
            self.monitoring.delete("9.8", "end")
            self.monitoring.insert(9.8, self.var_6.get())
            for file in os.listdir(self.get_FilePath()):

                if os.path.isdir(os.path.join(self.get_FilePath(), file)):
                    self.var_6.set(self.var_6.get() + "[DIR] " + file + "\n")
                
                else:
                    self.var_6.set(self.var_6.get() + "[FILE]" + file + str(
                        self.convert_size(os.path.getsize(os.path.join(self.get_FilePath(), file)))).rjust(
                        100 - len(file), '.') + "\n")

            self.var_6.set(self.var_6.get() + "\n")
            self.explorer.delete("1.0", "end")
            self.explorer.insert(2.1, self.var_6.get())
            self.explorer.config(state="disabled")
            self.select_file()

        # When there is no Drive or File in this computer
        except (FileNotFoundError, OSError):
            tkinter.messagebox.showinfo("Error", "There is No such Drive or File")
            FilePathList = []
            self.select_drive()
        self.entry.delete(0, 'end')

    def select_drive(self):
        self.button_start.config(state="disabled")
        self.var_6.set("")
        self.explorer.config(state="normal")
        self.var_6.set("Drives - " + ' / '.join(self.get_drives()) + "\n")
        self.var_6.set("Select drive\n" + self.var_6.get())
        # command
        self.entry.bind("<Return>", self.push)
        self.button_select = ttk.Button(self.pane_2, text="Select")
        self.button_select.bind('<Button-1>', self.push)
        self.button_select.grid(row=1, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")
        self.explorer.delete("1.0", "end")
        self.explorer.insert(2.1, self.var_6.get())
        self.explorer.config(state="disabled")

    def push(self, event=''):
        selected_drive = self.entry.get()
        if selected_drive.islower():
            selected_drive = selected_drive.upper()
        FilePathList.append(selected_drive + ':')
        self.print_FileList()

    # 탐색기
    def push2(self, event=''):
        global FilePathList
        selected_file = self.entry.get()
        if (selected_file.startswith('\'') and selected_file.endswith('\'')) or (
                selected_file.startswith('\"') and selected_file.endswith('\"')):
            selected_file = selected_file[1:len(selected_file) - 1]

        if selected_file == 'exit' or selected_file == 'quit':
            sys.exit()
        elif selected_file == 'ls' or selected_file == 'dir':
            self.print_FileList()
        elif selected_file == '..':
            if len(FilePathList) == 1:
                self.var_6.set(self.var_6.get() + "\nThere is no parent directory of" + FilePathList[0])
                self.select_file()
            else:
                FilePathList.pop(len(FilePathList) - 1)
                self.print_FileList()
        elif selected_file in os.listdir(self.get_FilePath()):
            if os.path.isdir(os.path.join(self.get_FilePath(), selected_file)):
                FilePathList.append(selected_file)
                self.print_FileList()
            else:
                FilePathList.append(selected_file)
                os.startfile(self.get_FilePath())
                FilePathList.pop(len(FilePathList) - 1)
                self.select_file()

        else:
            tkinter.messagebox.showinfo("Error", "There is No such Drive or File")
            self.select_file('retry')
        self.entry.delete(0, 'end')

    def select_file(self, word=''):
        if word == '':
            self.var_6.set(self.var_6.get() + "Select file or directory: ")
        self.explorer.config(state="normal")
        self.entry.bind("<Return>", self.push2)

        self.button_select = ttk.Button(self.pane_2, text="Select")
        self.button_select.bind('<Button-1>', self.push2)
        self.button_select.grid(row=1, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.explorer.delete("1.0", "end")
        self.explorer.insert(2.1, self.var_6.get())
        self.explorer.config(state="disabled")

    def read_csv(self, **kwds):
        f_types = [('CSV files', "*.csv"), ('All', "*.*")]
        file = filedialog.askopenfilename(filetypes=f_types)
        df = pd.read_csv(file)
        t = Toplevel()
        frame = Frame(t)
        frame.pack(fill=BOTH, expand=1)

        pt = MyTable(frame, dataframe=df, **kwds)
        pt.show()
        
    def rp_monitoring(self):
        global doMonitoring
        doMonitoring = True
        self.button_end2.config(state="normal")
        self.button_start2.config(state="disabled")
        global WATCHED_DIR
        if not doMonitoring:
            self.monitoring.config(state="disabled")
            
            FileData_Dataframe = pd.DataFrame(FileData)
            SavePath=str(WATCHED_DIR+"LiveScanLog.csv")
            FileData_Dataframe.to_csv(SavePath)

            if (self.var_1.get()):
                button=True

            else:
                button=False

            get_evtx('localhost', StartTime, button)
            return

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
            self.var_6.set("")
            self.var_6.set(self.var_6.get() + "Alert! File Action Alert!!\n")
            self.var_6.set(self.var_6.get() + FILE_ACTIONS.get(action, "Unknown") +"  "+ filename + "\n")
            FileData['Action'].append(FILE_ACTIONS.get(action, "Unknown"))
            FileData['File'].append(WATCHED_DIR + filename)
            self.var_6.set(self.var_6.get() + time.ctime() + "\n")
            FileData['Time'].append(time.ctime())
            self.var_6.set(self.var_6.get() + "---\n")
            self.monitoring.insert(self.cntline, self.var_6.get())
            self.cntline=self.cntline+4.0

        th1 = Thread(target = self.rp_monitoring)
        th1.start()

    def stop(self):
        global doMonitoring
        doMonitoring = False
        tkinter.messagebox.showinfo("End", "Finished monitoring\n The CSV is created in "+WATCHED_DIR)
        self.monitoring.insert(self.cntline, self.var_6.get())
        self.button_start2.config(state="normal")
        self.button_end2.config(state="disabled")

    def start(self):
        self.var_6.set("")
        self.monitoring.config(state="normal")
        self.monitoring.delete("1.0", "end")
        self.monitoring.insert(2.1, self.var_6.get())
        global doMonitoring
        doMonitoring = True
        self.button_end2.config(state="normal")
        self.button_start2.config(state="disabled")

    def setup_widgets(self):
        # Create a Frame for the Checkbuttons
        self.check_frame = ttk.LabelFrame(self, text="CSV Option", padding=(20, 10))
        self.check_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        # Checkbuttons
        self.check_2 = ttk.Checkbutton(
            self.check_frame, text="Save Detail", variable=self.var_1
        )
        self.check_2.grid(row=1, column=0, padx=5, pady=60, sticky="nsew")
       
        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Create a Frame for the Radiobuttons
        self.radio_frame = ttk.LabelFrame(self, text="Select Theme", padding=(20, 10))
        self.radio_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")

        # Radiobuttons
        self.radio_1 = ttk.Radiobutton(
            self.radio_frame, text="Light Theme", variable=self.var_3, value=1, command=change_theme
        )
        self.radio_1.grid(row=0, column=0, padx=3, pady=15, sticky="nsew")
        self.radio_2 = ttk.Radiobutton(
            self.radio_frame, text="Dark Theme", variable=self.var_3, value=2, command=change_theme
        )
        self.radio_2.grid(row=1, column=0, padx=3, pady=15, sticky="nsew")

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=1, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Notebook, pane #1
        self.notebook = ttk.Notebook(self.pane_1)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.tab_Introduce = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_Introduce.columnconfigure(index=index, weight=1)
            self.tab_Introduce.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_Introduce, text="Introduce")

        # Tab 1 -
        self.intro_proj = ttk.LabelFrame(self.tab_Introduce, text="Project", padding=(20, 10))
        self.intro_proj.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew", ipadx=200, ipady=30, columnspan=2
        )
        self.label_1 = ttk.Label(
            self.intro_proj,
            foreground='white',
            text="Project Link",
            justify="center",
            font=("-size", 15, "-weight", "bold", '-underline', True),
            anchor="center"
        )
        # self.label_1.config(fg='red')
        self.label_1.grid(row=0, column=0, pady=10, columnspan=2)

        def callback(url):
            webbrowser.open_new(url)

        self.label_1.bind("<Button-1>", lambda e: callback("https://github.com/persShins/22SysSecu-teamproject"))
        self.intro_schedule = ttk.LabelFrame(self.tab_Introduce, text="Member", padding=(20, 10))
        self.intro_schedule.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsew"
        )
        self.label_2 = ttk.Label(
            self.intro_schedule,
            text="2018270105 신원근\n2018270109 정성준\n2018270121 박재우\n2018270123 정현석\n2018270128 양승욱",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.label_2.grid(row=0, column=0, pady=10, columnspan=2)

        self.intro_team = ttk.LabelFrame(self.tab_Introduce, text="Notice", padding=(20, 10))
        self.intro_team.grid(
            row=1, column=1, padx=10, pady=10, sticky="nsew"
        )
        self.label_3 = ttk.Label(
            self.intro_team,
            text="Change Theme Using 'Select Theme' Frame\n In Step 1, there's a description of this program!",
            justify="center",
            font=("-size", 15, "-weight", "bold")
        )
        self.label_3.grid(row=0, column=0, pady=10, columnspan=2)

        # Tab #2
        self.tab_Explorer = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_Explorer, text="STEP 1")

        # Panedwindow
        self.paned = ttk.PanedWindow(self.tab_Explorer)
        self.paned.grid(row=0, column=3, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        self.explorer = tk.Text(
            self.pane_1,
            font=("-size", 10, "-weight", "bold"),
            yscrollcommand=self.scrollbar.set,
            height=20,
        )

        self.explorer.insert(tk.CURRENT, "How to Use\n\
1. Press \"Start Explorer\" Button to start!\n\
2. Select Directory that You Want to Monitoring!\n\
3. If You Finish Selected Path, then Press STEP 2 Tab\
")
        self.explorer.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.explorer.yview)

        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)
        self.button_start = ttk.Button(self.pane_2, text="Start Explorer", command=self.select_drive)
        self.button_start.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.entry = tk.Entry(self.pane_2, width=30)
        self.entry.grid(row=1, column=1, padx=(420, 10), pady=(20, 10), sticky="nsew")

        # Tab #3
        self.tab_Monitoring = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_Monitoring, text="STEP 2")

        # Panedwindow
        self.paned2 = ttk.PanedWindow(self.tab_Monitoring)
        self.paned2.grid(row=0, column=3, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane2 #1
        self.pane2_1 = ttk.Frame(self.paned2, padding=5)
        self.paned2.add(self.pane2_1, weight=1)

        # Scrollbar2
        self.scrollbar2 = ttk.Scrollbar(self.pane2_1)
        self.scrollbar2.pack(side="right", fill="y")

        self.monitoring = tk.Text(
            self.pane2_1,
            font=("-size", 10, "-weight", "bold"),
            yscrollcommand=self.scrollbar2.set,
            height=20,
        )

        self.monitoring.insert(tk.CURRENT, "How to Use\n\
1. Before Monitoring, Make Sure that the Path You Want to Monitor is Correct.\n\
2. Choose CSV Option (If You Check 'Save Detail', You Can Get More Information about Event Log in CSV file )\n\
3. Press \"Start Monitoring\" Button to Start!\n\
4. If You Want to Stop Monitoring, Press \"Stop Monitoring\" Button to Stop!\n\
5. After Monitoring, CSV files Will be Stored in the Current Path.\n\
6. If You Want to Read CSV files, Please Press STEP 3 Tab\n\n\
Current Path: C:\\")
        self.monitoring.pack(expand=True, fill="both")
        self.scrollbar2.config(command=self.monitoring.yview)

        self.pane2_2 = ttk.Frame(self.paned2, padding=5)
        self.paned2.add(self.pane2_2, weight=3)
        self.button_start2 = ttk.Button(self.pane2_2, text="Start Monitoring", command=self.start)
        self.button_start2.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.button_end2 = ttk.Button(self.pane2_2, text="Stop Monitoring", command=self.stop)
        self.button_end2.grid(row=1, column=1, padx=(450, 10), pady=(20, 10), sticky="nsew")
        self.button_end2.config(state="disabled")

        # Tab #4
        self.tab_EventLog = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_EventLog, text="STEP 3")
        self.button_start_csv = ttk.Button(self.tab_EventLog, text="Read csv file", command=self.read_csv)
        self.button_start_csv.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # Tab #5

        self.tab_Settings = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_Settings, text="Settings")

        # Remember, you have to use ttk widgets
        self.button = ttk.Button(self.tab_Settings, text="Change theme!", command=change_theme)
        self.button.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("18_0.0.1V")
    root.iconbitmap('./vaccine.ico')

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    root.mainloop()