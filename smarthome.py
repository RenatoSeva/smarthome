import tkinter as tk
from datetime import datetime, timedelta
from update_weather import update_weather
from toggle_light import toggle_light

api_key = 'ed4649c30926ba7ca03d8dfd36ef44b8'

root = tk.Tk()
root.title("Smart Home App")
root.configure(bg='#1E90FF')

top_banner = tk.Label(root, text="Welcome home", font=("Helvetica", 36), bg='#1E90FF', fg="white")
top_banner.pack(side="top")

temp_label = tk.Label(root, text="", font=("Helvetica", 18), bg='#1E90FF', fg="white")
temp_label.pack()

time_label = tk.Label(root, text="", font=("Helvetica", 18), bg='#1E90FF', fg="white")
time_label.pack()

left_frame = tk.Frame(root, bg='#1E90FF')
left_frame.pack(side='left')

city_label = tk.Label(left_frame, text="City:", font=("Helvetica", 12), bg='#1E90FF', fg="white")
city_label.pack()

city_entry = tk.Entry(left_frame)
city_entry.pack()

automation_enabled = tk.BooleanVar()
automation_enabled.set(True)

heating_status_label = tk.Label(left_frame, text="", font=("Helvetica", 12), bg='#1E90FF', fg="white")
heating_status_label.pack()

blinds_status_label = tk.Label(left_frame, text="", font=("Helvetica", 12), bg='#1E90FF', fg="white")
blinds_status_label.pack()

def toggle_automation():
    automation_enabled.set(not automation_enabled.get())
    if automation_enabled.get():
        automation_button.config(text="Automation: ON")
    else:
        automation_button.config(text="Automation: OFF")
        
def start_weather():
    update_weather(api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root, automation_enabled, light_statuses, light_buttons, light_status_label)
    local_time = datetime.now()
    local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
    update_label.config(text=f"Last update: {local_time_str}")
    root.after(60000, start_weather)
    
start_weather_button = tk.Button(left_frame, text="Update Weather", command=start_weather, bg='#1E90FF', fg="white")
start_weather_button.pack()

automation_button = tk.Button(left_frame, text="Automation: ON", command=toggle_automation, bg='#1E90FF', fg="white")
automation_button.pack()

update_label = tk.Label(left_frame, text="Last update: never", font=("Helvetica", 12), bg='#1E90FF', fg="white")
update_label.pack()

middle_frame = tk.Frame(root, bg='#1E90FF')
middle_frame.pack(side='left')

rooms = ['living room', 'dining room', 'kitchen', 'bathroom', 'bedroom', 'office']
light_statuses = {room: False for room in rooms}
light_status_label = {}
light_buttons = {}

for room in rooms:
    button_frame = tk.Frame(middle_frame, bg='#1E90FF')  
    button_frame.pack()

    button = tk.Button(button_frame, text=f"Toggle {room.capitalize()} Light", command=lambda r=room: toggle_light(r, light_statuses, light_buttons, light_status_label, automation_enabled, manual_override=False), bg="red", fg="white")
    button.pack(side='left')
    light_buttons[room] = button

    label = tk.Label(button_frame, text=f"{room.capitalize()} Light: OFF", font=("Helvetica", 12), bg='#1E90FF', fg="white")
    label.pack(side='left')
    light_status_label[room] = label

right_frame = tk.Frame(root, bg='#1E90FF')
right_frame.pack(side='left')

separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=5)

todo_list_frame = tk.Frame(root, bg='#1E90FF')
todo_list_frame.pack(side='left', padx=10, pady=10) 

def add_task(listbox, entry):
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        listbox.config(height=listbox.size())

for member in ['Mom', 'Dad', 'Kid']:
    member_frame = tk.Frame(todo_list_frame, bg='#1E90FF')
    member_frame.pack(side='top', padx=10, pady=10)
    member_label = tk.Label(member_frame, text=f"{member}'s To-Do List:", font=("Helvetica", 16), bg='#1E90FF', fg="white")
    member_label.pack(side='top', padx=10, pady=10)

    member_listbox = tk.Listbox(member_frame, font=("Helvetica", 12), bg='#1E90FF', fg="white", height=0)
    member_listbox.pack(side='top', padx=10, pady=10)

    member_entry = tk.Entry(member_frame)
    member_entry.pack(side='top', padx=10, pady=10)

    member_add_button = tk.Button(member_frame, text="Add Task", command=lambda lb=member_listbox, entry=member_entry: add_task(lb, entry))
    member_add_button.pack(side='top', padx=10, pady=10)

root.after(60000, update_weather, api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root, automation_enabled, light_statuses, light_buttons, light_status_label)

root.mainloop()
