import customtkinter as ctk
from datetime import datetime
from data import insert_data
import re
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk

def validate_integer(value):
    return re.match(r'^\d*$', value) is not None

def on_validate(P):
    return validate_integer(P)

def validate_datetime(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

app = ctk.CTk()
app.title("Twitter Comment Baiting Bot")
ctk.set_appearance_mode("dark")
app.attributes("-fullscreen")

def update_clock():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

def save_all():
    proxy = proxy_entry.get()
    signal = int(signal_entry.get()) if signal_entry.get() else 0
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    target = target_entry.get()
    event = event_entry.get()
    
    start_date = start_date_entry.get_date()
    start_time = f"{int(start_time_entry.get()):02d}:{int(start_minute_entry.get()):02d}:00"
    start_datetime = f"{start_date} {start_time}"
    
    end_date = end_date_entry.get_date()
    end_time = f"{int(end_time_entry.get()):02d}:{int(end_minute_entry.get()):02d}:00"
    end_datetime = f"{end_date} {end_time}"

    if not validate_datetime(start_datetime) or not validate_datetime(end_datetime):
        activities_text.insert(ctk.END, "Invalid date-time format. Please check your input.\n")
        return

    insert_data(proxy, username, password, email, target, event, signal, start_datetime, end_datetime)

    proxy_entry.delete(0, "end")
    signal_entry.delete(0, "end")
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")
    email_entry.delete(0, "end")
    target_entry.delete(0, "end")
    event_entry.delete(0, "end")
    start_date_entry.set_date(datetime.now().date())
    start_time_entry.set("00")
    start_minute_entry.set("00")
    end_date_entry.set_date(datetime.now().date())
    end_time_entry.set("00")
    end_minute_entry.set("00")

    activities_text.insert(ctk.END, "Data saved successfully\n")

# Set up the grid layout
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Clock Label at the top
clock_label = ctk.CTkLabel(app, text="", font=("Helvetica", 16))
clock_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

# Account Login
login_frame = ctk.CTkFrame(app, corner_radius=10)
login_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

username_label = ctk.CTkLabel(login_frame, text="Username:", font=("Helvetica", 14))
username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
username_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter username", width=200)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ctk.CTkLabel(login_frame, text="Password:", font=("Helvetica", 14))
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter password", show="*", width=200)
password_entry.grid(row=1, column=1, padx=10, pady=10)

email_label = ctk.CTkLabel(login_frame, text="Email:", font=("Helvetica", 14))
email_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
email_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter email", width=200)
email_entry.grid(row=2, column=1, padx=10, pady=10)

proxy_label = ctk.CTkLabel(login_frame, text="Proxy Address:", font=("Helvetica", 14))
proxy_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
proxy_entry = ctk.CTkEntry(login_frame, placeholder_text="e.g., 192.168.0.1:8080", width=200)
proxy_entry.grid(row=3, column=1, padx=10, pady=10)

signal_label = ctk.CTkLabel(login_frame, text="Signal time (seconds):", font=("Helvetica", 14))
signal_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
signal_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter the second for the tweet signal", width=200, 
                            validate="key", validatecommand=(app.register(on_validate), '%P'))
signal_entry.grid(row=4, column=1, padx=10, pady=10)

target_frame = ctk.CTkFrame(app, corner_radius=10)
target_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

target_label = ctk.CTkLabel(target_frame, text="Target Account URL:", font=("Helvetica", 14))
target_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
target_entry = ctk.CTkEntry(target_frame, placeholder_text="Enter target URL", width=400)
target_entry.grid(row=0, column=1, padx=10, pady=10)

event_label = ctk.CTkLabel(target_frame, text="Event:", font=("Helvetica", 14))
event_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
event_entry = ctk.CTkEntry(target_frame, placeholder_text="Enter event", width=400)
event_entry.grid(row=1, column=1, padx=10, pady=10)

start_time_label = ctk.CTkLabel(target_frame, text="Start Time:", font=("Helvetica", 14))
start_time_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
start_time_frame = ctk.CTkFrame(target_frame)
start_time_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
start_date_entry = DateEntry(start_time_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
start_date_entry.pack(side=tk.LEFT, padx=(0, 5))
start_time_entry = ttk.Spinbox(start_time_frame, from_=0, to=23, width=3, format="%02.0f")
start_time_entry.pack(side=tk.LEFT)
ttk.Label(start_time_frame, text=":").pack(side=tk.LEFT)
start_minute_entry = ttk.Spinbox(start_time_frame, from_=0, to=59, width=3, format="%02.0f")
start_minute_entry.pack(side=tk.LEFT)

end_time_label = ctk.CTkLabel(target_frame, text="End Time:", font=("Helvetica", 14))
end_time_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
end_time_frame = ctk.CTkFrame(target_frame)
end_time_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
end_date_entry = DateEntry(end_time_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
end_date_entry.pack(side=tk.LEFT, padx=(0, 5))
end_time_entry = ttk.Spinbox(end_time_frame, from_=0, to=23, width=3, format="%02.0f")
end_time_entry.pack(side=tk.LEFT)
ttk.Label(end_time_frame, text=":").pack(side=tk.LEFT)
end_minute_entry = ttk.Spinbox(end_time_frame, from_=0, to=59, width=3, format="%02.0f")
end_minute_entry.pack(side=tk.LEFT)

activities_frame = ctk.CTkFrame(app, corner_radius=10)
activities_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

activities_label = ctk.CTkLabel(activities_frame, text="Activities:", font=("Helvetica", 14))
activities_label.pack(pady=10)

activities_text = ctk.CTkTextbox(activities_frame, height=300, width=400)
activities_text.pack(pady=10)

button_save_all = ctk.CTkButton(app, text="Save All", command=save_all)
button_save_all.grid(row=3, column=0, columnspan=2, pady=20)

update_clock()
app.mainloop()