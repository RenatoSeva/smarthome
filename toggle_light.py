def toggle_light(room, light_statuses, light_buttons, light_status_label):
    light_status = light_statuses[room]
    if light_status:
        light_buttons[room].config(bg="red", fg="white")
        light_status_label[room].config(text=f"{room.capitalize()} Light: OFF")
    else:
        light_buttons[room].config(bg="green", fg="white")
        light_status_label[room].config(text=f"{room.capitalize()} Light: ON")
    light_statuses[room] = not light_status

def update_light_states(local_time, sunrise, sunset, light_statuses, light_buttons, light_status_label, weather_data):
    is_weekend = local_time.weekday() >= 5
    is_raining = weather_data.get("weather", [{}])[0].get("main", "").lower() == "rain"

    for room in light_statuses.keys():
        should_be_on = not is_weekend and (local_time >= sunset or local_time <= sunrise) or is_raining
        if should_be_on != light_statuses[room]:
            toggle_light(room, light_statuses, light_buttons, light_status_label)
