from datetime import datetime, timedelta
from weather_data import get_weather_data

def update_weather(api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root, automation_enabled, light_statuses, light_buttons, light_status_label):
    city = city_entry.get()
    if not city:
        city = "Zagreb"

    data = get_weather_data(city, api_key)

    if 'main' not in data:
        temp_label.config(text="Error: Invalid city")
        time_label.config(text="")
        heating_status_label.config(text="")
        blinds_status_label.config(text="")
    else:
        temperature = data['main']['temp']
        local_time = datetime.now()
        local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']) + timedelta(seconds=data['timezone'])
        sunset = datetime.fromtimestamp(data['sys']['sunset']) + timedelta(seconds=data['timezone'])
        weather_condition = data['weather'][0]['main'].lower()

        temp_label.config(text=f"Temperature: {temperature}°C")
        time_label.config(text=f"Local Time: {local_time_str}")

        if temperature < 14:
            heating_status_label.config(text="Heating Status: ON")
        else:
            heating_status_label.config(text="Heating Status: OFF")

        if sunrise <= local_time <= sunset and weather_condition != 'rain':
            blinds_status_label.config(text="Blinds Status: OPEN")
        else:
            blinds_status_label.config(text="Blinds Status: CLOSED")

        is_weekend = local_time.weekday() >= 5

        if not is_weekend:
            automation_enabled.set(True)
        else:
            automation_enabled.set(False)

        if automation_enabled.get():
            should_turn_on = (local_time >= sunset or local_time <= sunrise) or weather_condition == 'rain'
            for room in light_statuses.keys():
                if should_turn_on and not light_statuses[room]:
                    light_buttons[room].config(bg="green")
                    light_status_label[room].config(text=f"{room.capitalize()} Light: ON")
                    light_statuses[room] = True
                elif not should_turn_on and light_statuses[room]:
                    light_buttons[room].config(bg="red")
                    light_status_label[room].config(text=f"{room.capitalize()} Light: OFF")
                    light_statuses[room] = False

    root.after(60000, update_weather, api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root, automation_enabled, light_statuses, light_buttons, light_status_label)
