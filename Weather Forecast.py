import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import threading
import ttkbootstrap as ttk
import webbrowser

def get_weather(city):
    API_key = "5b26bdb6cd0cec4f6df1ffbf12e660b5"  # Replace with your actual API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp']
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']
    humidity = weather['main']['humidity']
    wind_speed = weather['wind']['speed']

    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country, humidity, wind_speed)

def search():
    city = city_entry.get()
    if city.strip() != "":
        loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        threading.Thread(target=fetch_and_display_weather, args=(city,)).start()

def fetch_and_display_weather(city):
    result = get_weather(city)
    if result is None:
        loading_label.place_forget()
        return

    icon_url, temperature, description, city, country, humidity, wind_speed = result
    location_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    wind_label.configure(text=f"Wind Speed: {wind_speed} m/s")
    loading_label.place_forget()

def open_link(url):
    # Specify the browser manually
    chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    webbrowser.get(chrome_path).open(url)

root = tk.Tk()
root.title("Weather Forecast")
root.geometry("500x500")

open_link('https://rishavweatherupdate.com')  # Open the link immediately when the script runs

# Custom Fonts
font_entry = ("Helvetica", 18)
font_label = ("Helvetica", 25)
font_weather_info = ("Helvetica", 20)

# Set background image
background_image = Image.open("cloud 2.jpg")  # Replace with your background image path
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Configure custom styles
style = ttk.Style()
style.configure('TEntry', font=font_entry)
style.configure('TButton', font=font_weather_info)

# Create an entry widget -> to enter the city name
city_entry = ttk.Entry(root, style='TEntry')
city_entry.pack(pady=20)

# Create a button widget -> to search for the weather information
search_button = ttk.Button(root, text="Search", command=search, bootstyle="success-outline", style='TButton')
search_button.pack(pady=10)

# Create a label widget -> to show the city/country name
location_label = tk.Label(root, font=font_label, bg="#e0f7fa")
location_label.pack(pady=10)

# Create a label widget -> to show the weather icon
icon_label = tk.Label(root, bg="#e0f7fa")
icon_label.pack()

# Create a label widget -> to show the temperature
temperature_label = tk.Label(root, font=font_weather_info, bg="#e0f7fa")
temperature_label.pack()

# Create a label widget -> to show the weather description
description_label = tk.Label(root, font=font_weather_info, bg="#e0f7fa")
description_label.pack()

# Create additional labels for humidity and wind speed
humidity_label = tk.Label(root, font=font_weather_info, bg="#e0f7fa")
humidity_label.pack()
wind_label = tk.Label(root, font=font_weather_info, bg="#e0f7fa")
wind_label.pack()

# Loading label
loading_label = tk.Label(root, text="Loading...", font=font_weather_info, bg="#e0f7fa")

root.mainloop()


