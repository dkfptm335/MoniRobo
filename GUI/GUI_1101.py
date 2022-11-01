from msilib.schema import File
import tkinter as tk
import os
import tkinter
import win32file
import win32process
import string
import sys
import math
from ctypes import windll
from tkinter import ttk
from tkhtmlview import HTMLLabel
import webbrowser
import tkinter.messagebox

FilePathList = []
FilePath = None


def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")


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
        # self.var_7 = tk.StringVar()

        # Create widgets :)
        self.setup_widgets()

    def get_FilePath(self):
        if len(FilePathList) == 1 and (FilePathList[0] == 'C:' or FilePathList[0] == 'D:' or FilePathList[0] == "E:"
                                       or FilePathList[0] == "F:" or FilePathList[0] == "G:" or FilePathList[
                                           0] == "H:"):
            return FilePathList[0] + '\\'

        else:
            FilePath = '\\'.join(FilePathList)
            return FilePath

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
            for file in os.listdir(self.get_FilePath()):

                if os.path.isdir(os.path.join(self.get_FilePath(), file)):
                    # print("[DIR] ", file, str(convert_size(get_dirsize(file))).rjust(100-len(file), '.'))
                    self.var_6.set(self.var_6.get() + "[DIR] " + file + "\n")
                    # print("[DIR] ", file)
                else:
                    self.var_6.set(self.var_6.get() + "[FILE]" + file + str(
                        self.convert_size(os.path.getsize(os.path.join(self.get_FilePath(), file)))).rjust(
                        100 - len(file), '.') + "\n")
                    # print("[FILE]", file, str(self.convert_size(os.path.getsize(file))).rjust(120 - len(file), '.'))
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

    def setup_widgets(self):
        # Create a Frame for the Checkbuttons
        self.check_frame = ttk.LabelFrame(self, text="Checkbuttons", padding=(20, 10))
        self.check_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        # Checkbuttons
        self.check_1 = ttk.Checkbutton(
            self.check_frame, text="Unchecked", variable=self.var_0
        )
        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.check_2 = ttk.Checkbutton(
            self.check_frame, text="Checked", variable=self.var_1
        )
        self.check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.check_3 = ttk.Checkbutton(
            self.check_frame, text="Third state", variable=self.var_2
        )
        self.check_3.state(["alternate"])
        self.check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.check_4 = ttk.Checkbutton(
            self.check_frame, text="Disabled", state="disabled"
        )
        self.check_4.state(["disabled !alternate"])
        self.check_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Create a Frame for the Radiobuttons
        self.radio_frame = ttk.LabelFrame(self, text="Radiobuttons", padding=(20, 10))
        self.radio_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")

        # Radiobuttons
        self.radio_1 = ttk.Radiobutton(
            self.radio_frame, text="Unselected", variable=self.var_3, value=1
        )
        self.radio_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_2 = ttk.Radiobutton(
            self.radio_frame, text="Selected", variable=self.var_3, value=2
        )
        self.radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_4 = ttk.Radiobutton(
            self.radio_frame, text="Disabled", state="disabled"
        )
        self.radio_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

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
        self.intro_schedule = ttk.LabelFrame(self.tab_Introduce, text="Schedule", padding=(20, 10))
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

        self.intro_team = ttk.LabelFrame(self.tab_Introduce, text="Team", padding=(20, 10))
        self.intro_team.grid(
            row=1, column=1, padx=10, pady=10, sticky="nsew"
        )
        self.label_3 = ttk.Label(
            self.intro_team,
            text="2018270105 신원근\n2018270109 정성준\n2018270121 박재우\n2018270123 정현석\n2018270128 양승욱",
            justify="center",
            font=("-size", 15, "-weight", "bold")
        )
        self.label_3.grid(row=0, column=0, pady=10, columnspan=2)

        # Tab #2
        self.tab_Explorer = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_Explorer, text="Explorer")

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

        self.explorer.insert(tk.CURRENT, "Press \"Start Explore\" Button to start!")
        self.explorer.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.explorer.yview)

        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)
        self.button_start = ttk.Button(self.pane_2, text="Start Explore", command=self.select_drive)
        self.button_start.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.entry = tk.Entry(self.pane_2, width=30)
        self.entry.grid(row=1, column=1, padx=(420, 10), pady=(20, 10), sticky="nsew")

        # Tab #3
        self.tab_Monitoring = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_Monitoring, text="Monitoring")

        # Tab #4
        self.tab_Settings = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_Settings, text="Settings")

        self.settings_frame = ttk.LabelFrame(self, text="settings_frame", padding=(20, 10))
        self.settings_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        # Remember, you have to use ttk widgets
        self.button = ttk.Button(self.tab_Settings, text="Change theme!", command=change_theme)
        self.button.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
        # button.pack()

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