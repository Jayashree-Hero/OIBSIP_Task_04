import tkinter as tk
from tkinter import messagebox
import requests
from geopy.geocoders import Nominatim
from datetime import datetime

API_KEY = '29fd4e16609044dd0c7ee41e27f23a3b'

def get_weather_data(location):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast_data(location):
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("400x600")
        self.configure(bg="#98FB98") 
        self.create_widgets()

    def create_widgets(self):
        label_style = {'bg': "#98FB98", 'font': ("Helvetica", 12, "bold")}

        tk.Label(self, text="Location:", **label_style).grid(row=0, column=0, pady=10, padx=10)
        self.location_entry = tk.Entry(self)
        self.location_entry.grid(row=0, column=1, pady=10, padx=10)

        button_style = {'bg': "#32CD32", 'fg': "white", 'font': ("Helvetica", 10, "bold"), 'width': 15, 'height': 1}
        tk.Button(self, text="Get Weather", command=self.on_get_weather, **button_style).grid(row=1, columnspan=2, pady=10)
        
        self.canvas = tk.Canvas(self, bg="#98FB98")
        self.canvas.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=2, column=2, sticky="ns")
        
        self.weather_frame = tk.Frame(self.canvas, bg="#98FB98")
        self.canvas.create_window((0,0), window=self.weather_frame, anchor="nw")
        self.weather_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_get_weather(self):
        location = self.location_entry.get()
        if location:
            weather_data = get_weather_data(location)
            forecast_data = get_forecast_data(location)
            if weather_data and forecast_data:
                self.display_weather(weather_data, forecast_data)
            else:
                messagebox.showerror("Error", "Unable to fetch weather data. Please check your location or API key.")
        else:
            messagebox.showerror("Input Error", "Please enter a location.")

    def display_weather(self, weather_data, forecast_data):
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        if weather_data.get('cod') != 200:
            messagebox.showerror("Error", "Unable to fetch weather data.")
            return

        current_weather = weather_data['weather'][0]
        temp = weather_data['main']['temp']
        wind_speed = weather_data['wind']['speed']
        description = current_weather['description']
        icon = current_weather['icon']

        icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
        icon_response = requests.get(icon_url)
        icon_image = tk.PhotoImage(data=icon_response.content)

        label_style = {'bg': "#98FB98", 'font': ("Helvetica", 12)}

        tk.Label(self.weather_frame, text=f"Current Weather in {weather_data['name']}", **label_style).grid(row=0, column=0, columnspan=2)
        tk.Label(self.weather_frame, text=f"{description.capitalize()}", **label_style).grid(row=1, column=0)
        tk.Label(self.weather_frame, image=icon_image, **label_style).grid(row=1, column=1)
        tk.Label(self.weather_frame, text=f"Temperature: {temp}°C", **label_style).grid(row=2, column=0, columnspan=2)
        tk.Label(self.weather_frame, text=f"Wind Speed: {wind_speed} m/s", **label_style).grid(row=3, column=0, columnspan=2)

        self.icon_image = icon_image

        for i in range(5):
            forecast = forecast_data['list'][i]
            date_text = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
            forecast_desc = forecast['weather'][0]['description']
            forecast_temp = forecast['main']['temp']
            forecast_wind_speed = forecast['wind']['speed']
            forecast_icon = forecast['weather'][0]['icon']

            forecast_icon_url = f"http://openweathermap.org/img/wn/{forecast_icon}.png"
            forecast_icon_response = requests.get(forecast_icon_url)
            forecast_icon_image = tk.PhotoImage(data=forecast_icon_response.content)

            tk.Label(self.weather_frame, text=date_text, **label_style).grid(row=4+i*4, column=0, columnspan=2)
            tk.Label(self.weather_frame, text=f"{forecast_desc.capitalize()}", **label_style).grid(row=5+i*4, column=0)
            tk.Label(self.weather_frame, image=forecast_icon_image, **label_style).grid(row=5+i*4, column=1)
            tk.Label(self.weather_frame, text=f"Temp: {forecast_temp}°C", **label_style).grid(row=6+i*4, column=0, columnspan=2)
            tk.Label(self.weather_frame, text=f"Wind: {forecast_wind_speed} m/s", **label_style).grid(row=7+i*4, column=0, columnspan=2)

            setattr(self, f"forecast_icon_image_{i}", forecast_icon_image)

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()

