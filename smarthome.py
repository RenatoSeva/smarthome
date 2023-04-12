import tkinter as tk
from datetime import datetime, timedelta
from update_weather import update_weather
from toggle_light import toggle_light

api_key = 'ed4649c30926ba7ca03d8dfd36ef44b8'

root = tk.Tk()
root.title("Smart Home App")
root.configure(bg='#1E90FF')

top_banner = tk.Label(root, text="Hello", font=("Helvetica", 18), bg='#1E90FF', fg="white")
top_banner.pack(side="top")

left_frame = tk.Frame(root, bg='#1E90FF')
left_frame.pack(side='left')

city_label = tk.Label(left_frame, text="City:", font=("Helvetica", 12), bg='#1E90FF', fg="white")
city_label.pack()

city_entry = tk.Entry(left_frame)
city_entry.pack()

temp_label = tk.Label(left_frame, text="", font=("Helvetica", 12), bg='#1E90FF', fg="white")
temp_label.pack()

time_label = tk.Label(left_frame, text="", font=("Helvetica", 12), bg='#1E90FF', fg="white")
time_label.pack()

heating_status_label = tk.Label(left_frame, text="", font=("Helvetica", 12), bg='#1E90FF', fg="white")
heating_status_label.pack()

blinds_status_label = tk.Label(left_frame, text="", font=("Helvetica", 12), bg='#1E90FF', fg="white")
blinds_status_label.pack()

right_frame = tk.Frame(root, bg='#1E90FF')
right_frame.pack(side='right')

rooms = ['living room', 'dining room', 'kitchen', 'bathroom', 'bedroom', 'office']
light_statuses = {room: False for room in rooms}
light_status_label = {}
light_buttons = {}

def start_weather():
    update_weather(api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root)
    root.after(60000, update_weather, api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root)

update_button = tk.Button(left_frame, text="Update Weather", command=start_weather, bg='#1E90FF', fg="white")
update_button.pack()

for room in rooms:
    button = tk.Button(right_frame, text=f"Toggle {room.capitalize()} Light", command=lambda r=room: toggle_light(r, light_statuses, light_buttons, light_status_label), bg="red", fg="white")
    button.pack()
    light_buttons[room] = button

    label = tk.Label(right_frame, text=f"{room.capitalize()} Light: OFF", font=("Helvetica", 12), bg='#1E90FF', fg="white")
    label.pack()
    light_status_label[room] = label

update_weather(api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root)

root.mainloop()