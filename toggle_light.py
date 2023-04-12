def toggle_light(room, light_statuses, light_buttons, light_status_label):
    light_status = light_statuses[room]
    if light_status:
        light_buttons[room].config(bg="red")
        light_status_label[room].config(text=f"{room.capitalize()} Light: OFF")
    else:
        light_buttons[room].config(bg="green")
        light_status_label[room].config(text=f"{room.capitalize()} Light: ON")
    light_statuses[room] = not light_status
