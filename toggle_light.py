def toggle_light(room, light_statuses, light_buttons, light_status_label, automation_enabled, manual_override=False):
    if not automation_enabled.get():  # Dodata provjera za automatsko upravljanje
        light_status = light_buttons[room].cget('bg') == "green"

        if light_status:
            light_buttons[room].config(bg="red", fg="white")
            light_status_label[room].config(text=f"{room.capitalize()} Light: OFF")
        else:
            light_buttons[room].config(bg="green", fg="white")
            light_status_label[room].config(text=f"{room.capitalize()} Light: ON")

        light_statuses[room] = light_buttons[room].cget('bg') == "green"

def update_light_states(local_time, sunrise, sunset, light_statuses, light_buttons, light_status_label, automation_enabled, is_raining):
    is_weekend = local_time.weekday() >= 5

    for room in light_statuses.keys():
        should_be_on = automation_enabled.get() and not is_weekend and sunrise <= local_time <= sunset
        if should_be_on != light_statuses[room]:
            toggle_light(room, light_statuses, light_buttons, light_status_label, automation_enabled)

    if is_raining:
        for room in light_statuses.keys():
            if not light_statuses[room]:
                toggle_light(room, light_statuses, light_buttons, light_status_label, automation_enabled)
