import win32profile
import win32file

profile = win32profile.GetProfilesDirectory()
print("User Profile Directory >", profile, '\n')

dir = 'C:\\'

print("[Disk Free Space]")
freespace = win32file.GetDiskFreeSpace(dir)
print('Sectors per cluster: ' + str(freespace[0]))
print('Bytes per sector: ' + str(freespace[1]))
print('Number of free clusters: ' + str(freespace[2]))
print('Total number of clusters: ' + str(freespace[3]))
freespace = win32file.GetDiskFreeSpaceEx(dir)
print('freeBytes: ' + str(freespace[0]))
print('totalBytes: ' + str(freespace[1]))
print('totalFreeBytes: ' + str(freespace[2]))
print('\n')