import os, os.path
import win32file
import win32process

dir = 'C:\\'
files = os.listdir(dir)

for file in files:
    file = os.path.join(dir, file)

    if os.path.isdir(file):
        fullname_file = os.path.join(dir, file)
        print('[directory] ' + fullname_file)
    else:
        fullname_file = os.path.join(dir, file)
        print('[  file   ] ' + fullname_file)

print('\n')

freespace = win32file.GetDiskFreeSpace(dir)
print('Sectors per cluster: ' + str(freespace[0]))
print('Bytes per sector: ' + str(freespace[1]))
print('Number of free clusters: ' + str(freespace[2]))
print('Total number of clusters: ' + str(freespace[3]))
print('\n')

freespace = win32file.GetDiskFreeSpaceEx(dir)
print('freeBytes: ' + str(freespace[0]))
print('totalBytes: ' + str(freespace[1]))
print('totalFreeBytes: ' + str(freespace[2]))
print('\n')

Current_Process = win32process.GetCurrentProcess()
PID = win32process.GetProcessId(Current_Process)
print('Current Process ID: ' + str(PID)) 

print('\n')

current_process_info = win32process.GetProcessMemoryInfo(Current_Process)
for info_key, info_value in current_process_info.items():
    print("{0:<27}".format(info_key), "{0:>10}".format(info_value))