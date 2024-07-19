import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import customtkinter as ctk
from data import *
import subprocess
from threading import Thread
from services.main import main
import schedule
import time
from datetime import datetime

# Dictionary to keep track of running events
running_events = {}

def run_event(event):
    event_id = event[0]
    url = event[5]
    proxy = event[1]
    email = event[4]
    password = event[3]
    signal_time = event[7]
    end_time = datetime.strptime(event[9], "%Y-%m-%d %H:%M:%S")

    def job():
        if datetime.now() < end_time and event_id in running_events:
            try:
                main(url, proxy, email, password, signal_time)
            except Exception as e:
                print(f"Error running main: {str(e)}")
        else:
            return schedule.CancelJob

    schedule.every(1).minutes.do(job)

    while datetime.now() < end_time and event_id in running_events:
        schedule.run_pending()
        time.sleep(1)

    if event_id in running_events:
        del running_events[event_id]
    app.after(0, update_events_frame)  # Schedule GUI update on main thread

def start_event(event_id):
    event = get_by_id(event_id)
    if event and event_id not in running_events:
        start_time = datetime.strptime(event[8], "%Y-%m-%d %H:%M:%S")
        
        if start_time > datetime.now():
            def schedule_start():
                time.sleep((start_time - datetime.now()).total_seconds())
                if event_id in running_events:
                    Thread(target=run_event, args=(event,)).start()

            running_events[event_id] = Thread(target=schedule_start)
            running_events[event_id].start()
        else:
            running_events[event_id] = Thread(target=run_event, args=(event,))
            running_events[event_id].start()
        
        update_events_frame()

def stop_event(event_id):
    if event_id in running_events:
        del running_events[event_id]
        update_events_frame()

def delete(event_id):
    stop_event(event_id)
    delete_event(event_id)  # Make sure this function is defined or imported
    update_events_frame()

app = ctk.CTk()
app.title("Events Page")
ctk.set_appearance_mode("dark")
app.minsize(height=400, width=600)

def open_new_event():
    subprocess.Popen(['python', os.path.join(os.path.dirname(__file__), 'new.py')])

def update_events_frame():
    for widget in events_frame.winfo_children():
        widget.destroy()

    global events
    events = get_data()

    for event in events:
        event_frame = ctk.CTkFrame(events_frame)
        event_frame.pack(pady=5, padx=10, fill="x")

        event_label = ctk.CTkLabel(event_frame, text=event[6], font=("Helvetica", 14))
        event_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        start_button = ctk.CTkButton(event_frame, text="Start", command=lambda e_id=event[0]: start_event(e_id))
        start_button.grid(row=0, column=1, padx=5, pady=10)

        stop_button = ctk.CTkButton(event_frame, text="Stop", command=lambda e_id=event[0]: stop_event(e_id))
        stop_button.grid(row=0, column=2, padx=5, pady=10)

        delete_button = ctk.CTkButton(event_frame, text="Delete", command=lambda e_id=event[0]: delete(e_id))
        delete_button.grid(row=0, column=3, padx=5, pady=10)

        status_label = ctk.CTkLabel(event_frame, text="Running" if event[0] in running_events else "Stopped", font=("Helvetica", 12))
        status_label.grid(row=0, column=4, padx=10, pady=10)

title_label = ctk.CTkLabel(app, text="Events Page", font=("Helvetica", 24, "bold"))
title_label.pack(pady=20)

events_frame = ctk.CTkFrame(app)
events_frame.pack(pady=20, padx=20, fill="both", expand=True)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

add_event_button = ctk.CTkButton(button_frame, text="Add Event", command=open_new_event)
add_event_button.pack(side="left", padx=5)

refresh_button = ctk.CTkButton(button_frame, text="Refresh", command=update_events_frame)
refresh_button.pack(side="left", padx=5)

update_events_frame()

app.mainloop()