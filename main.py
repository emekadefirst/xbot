import os
import subprocess
import customtkinter as ctk
from datetime import datetime
import psutil

subprocesses = []

def open_new():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.join(script_dir, "new.py")
    p = subprocess.Popen(["python", new_path])
    subprocesses.append(p)

def open_continue():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    continue_path = os.path.join(script_dir, "continue.py")
    p = subprocess.Popen(["python", continue_path])
    subprocesses.append(p)

def update_clock():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clock_label.configure(text=now)
    app.after(1000, update_clock) 

def on_close():
    for p in subprocesses:
        try:
            process = psutil.Process(p.pid)
            for proc in process.children(recursive=True):
                proc.terminate()
            process.terminate()
        except psutil.NoSuchProcess:
            pass
    app.destroy()

app = ctk.CTk()
app.title("Xbot Tool app")
ctk.set_appearance_mode("dark")
app.minsize(height=400, width=400)
app.maxsize(height=400, width=400)

head = ctk.CTkLabel(app, text="Welcome Back!", fg_color="transparent")
head.pack()
prompt = ctk.CTkLabel(app, text="What would you like to do", fg_color="transparent")
prompt.pack()
clock_label = ctk.CTkLabel(app, text="", font=("Helvetica", 16))
clock_label.pack(pady=10)

Start = ctk.CTkButton(app, text="Add new event", command=open_new)
Start.pack(padx=20, pady=10)

continue_event = ctk.CTkButton(app, text="Continue event", command=open_continue)
continue_event.pack(padx=20, pady=10)

update_clock()

app.protocol("WM_DELETE_WINDOW", on_close)

app.mainloop()
