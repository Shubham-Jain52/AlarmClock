import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time
import pygame

pygame.mixer.init()


time_input = ''
alarm_time = ''
alarm_running = False
alarm_triggered = False  

def on_click(val):
    global time_input
    time_input += str(val)
    text_disp.config(text=time_input)

def clear():
    global time_input
    time_input = ''
    text_disp.config(text="")

def backspace():
    global time_input
    time_input = time_input[:-1]
    text_disp.config(text=time_input)

def play_alarm_sound():
    global alarm_running
    audio_path = r"Enter\Your\file\path\here"
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)  
        alarm_running = True
    except Exception as e:
        messagebox.showerror("Error", f"Could not play alarm sound:\n{e}")

def stop_alarm():
    global alarm_running
    if alarm_running:
        pygame.mixer.music.stop()
        alarm_running = False
        messagebox.showinfo("Alarm", "Alarm stopped.")

def show_alarm_message():
    messagebox.showinfo("Alarm", f"WAKE UP! It's {alarm_time}")

def alarm_check():
    global alarm_time, alarm_running, alarm_triggered
    while True:
        now = datetime.now().strftime("%H:%M")
        if alarm_time:
            if now == alarm_time and not alarm_running and not alarm_triggered:
                play_alarm_sound()
                alarm_triggered = True
             
                window.after(0, show_alarm_message)
            elif now != alarm_time:
               
                alarm_triggered = False
        time.sleep(1)

def set_alarm():
    global time_input, alarm_time
    if len(time_input) == 4 and time_input.isdigit():
        hours = int(time_input[:2])
        mins = int(time_input[2:])
        if 0 <= hours <= 23 and 0 <= mins <= 59:
            alarm_time = f"{hours:02d}:{mins:02d}"
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
            clear()
        else:
            messagebox.showerror("Invalid", "Enter time in 24-hr format (HHMM)")
    else:
        messagebox.showerror("Invalid", "Enter time in 24-hr format (HHMM)")

def update_live_clock():
    now = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=f"Current Time: {now}")
    window.after(1000, update_live_clock)

# GUI Setup
window = tk.Tk()
window.title("Alarm Clock")
window.geometry("400x600")
window.resizable(False, False)
window.config(bg="black")

# Top display
tk.Label(window, text='Enter Alarm Time (HHMM):', font=("Arial", 14), bg="black", fg="white").pack(pady=10)
text_disp = tk.Label(window, text="", font=('Arial', 24, 'bold'), width=10, bg="white", relief=tk.RAISED)
text_disp.pack(pady=10)

# Clock
clock_label = tk.Label(window, text="", font=("Arial", 16), fg="lime", bg="black")
clock_label.pack(pady=10)

# Button grid
btn_frame = tk.Frame(window, bg="black")
btn_frame.pack(pady=20)

btn_texts = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['CLEAR', '0', 'DEL']
]

for row_index, row in enumerate(btn_texts):
    for col_index, item in enumerate(row):
        if item == 'CLEAR':
            cmd = clear
        elif item == 'DEL':
            cmd = backspace
        else:
            cmd = lambda t=item: on_click(t)
        tk.Button(btn_frame, text=item, width=10, height=2, font=("Arial", 12),
                  command=cmd).grid(row=row_index, column=col_index, padx=5, pady=5)


tk.Button(window, text="SET ALARM", font=("Arial", 14, 'bold'), width=20, bg="green", fg="white",
          command=set_alarm).pack(pady=10)
tk.Button(window, text="STOP ALARM", font=("Arial", 14, 'bold'), width=20, bg="red", fg="white",
          command=stop_alarm).pack(pady=10)


update_live_clock()
threading.Thread(target=alarm_check, daemon=True).start()

window.mainloop()
