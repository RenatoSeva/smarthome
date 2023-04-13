from weather_data import get_weather_data
from datetime import datetime, timedelta
from toggle_light import toggle_light

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
        local_time = datetime.now()
        local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
        temperature = data['main']['temp']
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']) + timedelta(seconds=data['timezone'])
        sunset = datetime.fromtimestamp(data['sys']['sunset']) + timedelta(seconds=data['timezone'])
        weather = data.get("weather", [{}])[0].get("main", "").lower()

        temp_label.config(text=f"Temperature: {temperature}°C")
        time_label.config(text=f"Local Time: {local_time_str}")

        if temperature < 14:
            heating_status_label.config(text="Heating Status: ON")
        else:
            heating_status_label.config(text="Heating Status: OFF")

        if weather == "rain":
            is_raining = True
        else:
            is_raining = False

        is_weekend = local_time.weekday() >= 5

        for room in light_statuses.keys():
            should_be_on = (automation_enabled.get() and not is_weekend and ((local_time >= sunset or local_time <= sunrise) or is_raining or light_statuses[room]))
            if should_be_on != light_statuses[room]:
                toggle_light(room, light_statuses, light_buttons, light_status_label, automation_enabled)

        if sunrise <= local_time <= sunset and not is_raining:
            blinds_status_label.config(text="Blinds Status: OPEN")
        else:
            blinds_status_label.config(text="Blinds Status: CLOSED")

    root.after(60000, update_weather, api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root, automation_enabled, light_statuses, light_buttons, light_status_label)
