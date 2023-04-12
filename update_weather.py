from datetime import datetime, timedelta
from weather_data import get_weather_data

def update_weather(api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root):
    city = city_entry.get()
    if not city:
        city = "Zagreb"

    data = get_weather_data(city, api_key)

    if 'main' not in data:
        temp_label.config(text="Error: Invalid city or API key")
        time_label.config(text="")
        heating_status_label.config(text="")
        blinds_status_label.config(text="")
    else:
        temperature = data['main']['temp']
        local_time = datetime.now()
        local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']) + timedelta(seconds=data['timezone'])
        sunset = datetime.fromtimestamp(data['sys']['sunset']) + timedelta(seconds=data['timezone'])

        temp_label.config(text=f"Temperature: {temperature}°C")
        time_label.config(text=f"Local Time: {local_time_str}")

        if temperature < 14:
            heating_status_label.config(text="Heating Status: ON")
        else:
            heating_status_label.config(text="Heating Status: OFF")

        if sunrise <= local_time <= sunset:
            blinds_status_label.config(text="Blinds Status: OPEN")
        else:
            blinds_status_label.config(text="Blinds Status: CLOSED")
    
    root.after(60000, update_weather, api_key, city_entry, temp_label, time_label, heating_status_label, blinds_status_label, root)