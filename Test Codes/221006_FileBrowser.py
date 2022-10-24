from ctypes import windll
import os, os.path
import string
import sys
import math

FilePathList = []
FilePath = None

def get_FilePath():
    if len(FilePathList) == 1 and (FilePathList[0] == 'C:' or FilePathList[0] == 'D:' or FilePathList[0] == "E:" 
                                   or FilePathList[0] == "F:" or FilePathList[0] == "G:" or FilePathList[0] == "H:"):
        return FilePathList[0] + '\\'

    else:
        FilePath = '\\'.join(FilePathList)
        return FilePath

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter + ':')
        bitmask >>= 1
    return drives

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def get_dirsize(start_path = '.'):
    total_size = 0
    for dirpath, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def print_FileList():
    print("Path:", get_FilePath())
    
    for file in os.listdir(get_FilePath()):
        if os.path.isdir(os.path.join(get_FilePath(), file)):
            #print("[DIR] ", file, str(convert_size(get_dirsize(file))).rjust(100-len(file), '.'))
            print("[DIR] ", file)
        else:
            print("[FILE]", file, str(convert_size(os.path.getsize(os.path.join(get_FilePath(), file)))).rjust(80-len(file), '.'))

def select_drive():
    print("Drives:", get_drives())
    selected_drive = input("Select drive: ")
    if selected_drive.islower():
        selected_drive = selected_drive.upper()
    FilePathList.append(selected_drive + ':')
    
    print_FileList()
         
def select_file():
    selected_file = input("Select file or directory: ")
    if (selected_file.startswith('\'') and selected_file.endswith('\'')) or (selected_file.startswith('\"') and selected_file.endswith('\"')):
        selected_file = selected_file[1:len(selected_file) - 1]
    
    if selected_file == 'exit' or selected_file == 'quit':
        sys.exit()
    elif selected_file == 'ls' or selected_file == 'dir':
        print_FileList()
        select_file()  
    elif selected_file == '..':
        if len(FilePathList) == 1:
            print("There is no parent directory of", FilePathList[0])
            select_file()
        else:
            FilePathList.pop(len(FilePathList) - 1)
            print_FileList()
            select_file()  
    elif selected_file in os.listdir(get_FilePath()):
        if os.path.isdir(os.path.join(get_FilePath(), selected_file)):
            FilePathList.append(selected_file)
            print_FileList()
            select_file()
        else:
            FilePathList.append(selected_file)
            os.startfile(get_FilePath())
            FilePathList.pop(len(FilePathList) - 1)
            select_file()
    else:
        print("There is no directory or file named", selected_file, "in this directory, please re-input")
        select_file()
        
if __name__ == '__main__':
    select_drive()
    select_file()
