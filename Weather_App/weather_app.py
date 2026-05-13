import tkinter as tk
from tkinter import messagebox
from turtle import bgcolor
import requests

# =========================
# API KEY
# =========================
API_KEY = "2277b6f734564f587648b586af376477"

# Default Unit
unit = "metric"


bg_color = "#95a5a6"

# =========================
# WEATHER THEME
# =========================
def get_theme(condition):

    condition = condition.lower()

    if "clear" in condition:
        return "#f7c948"

    elif "cloud" in condition:
        return "#95a5a6"

    elif "rain" in condition:
        return "#5d6d7e"

    elif "snow" in condition:
        return "#dfe6e9"

    else:
        return "#74b9ff"

# =========================
# CURRENT WEATHER
# =========================
def get_weather():

    city = city_entry.get()

    if city == "":
        messagebox.showerror("Error", "Please enter city name")
        return

    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}"

    try:

        data = requests.get(current_url).json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found")
            return

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]

        condition = data["weather"][0]["main"]

        bg_color = get_theme(condition)

        # Change Background
        root.configure(bg=bg_color)
        main_frame.configure(bg=bg_color)

        city_label.config(
            text=city.upper(),
            bg=bg_color
        )

        symbol = "°C" if unit == "metric" else "°F"
        temp_label.config(
            text=f"{temp:.1f}{symbol}",
            bg=bg_color
        )

        desc_label.config(
            text=condition,
            bg=bg_color
        )

        details_label.config(
            text=f"Feels Like: {feels:.1f}°C\n"
                 f"Min Temp: {temp_min:.1f}°C\n"
                 f"Max Temp: {temp_max:.1f}°C\n"
                 f"Humidity: {humidity}%\n"
                 f"Wind Speed: {wind} m/s",
            bg=bg_color
        )

        get_forecast(city, bg_color)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# =========================
# FORECAST FUNCTION
# =========================
def get_forecast(city, bg_color):

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={unit}"

    try:

        data = requests.get(forecast_url).json()

        # Clear old cards
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        # =========================
        # HOURLY FORECAST
        # =========================
        for item in data["list"][:5]:

            time = item["dt_txt"][11:16]

            temp = item["main"]["temp"]

            condition = item["weather"][0]["main"]

            # Weather Text
            if "Cloud" in condition:
                weather_icon = "Cloudy"

            elif "Rain" in condition:
                weather_icon = "Rainy"

            elif "Clear" in condition:
                weather_icon = "Sunny"

            else:
                weather_icon = condition

            # Forecast Card
            card = tk.Frame(
                forecast_frame,
                bg="white",
                width=120,
                height=140,
                bd=2,
                relief="ridge"
            )

            card.grid(row=0, column=data["list"][:5].index(item), padx=10)

            

            # Time
            tk.Label(
                card,
                text=time,
                font=("Arial", 13, "bold"),
                bg="white",
                fg="#2c3e50"
            ).pack(pady=8)

            # Weather
            tk.Label(
                card,
                text=weather_icon,
                font=("Arial", 11),
                bg="white",
                fg="#34495e"
            ).pack(pady=5)

            # Temperature
            tk.Label(
                card,
                text=f"{temp:.1f}°C",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#e67e22"
            ).pack(pady=10)

            # Condition
            tk.Label(
                card,
                text=condition,
                font=("Arial", 10),
                bg="white",
                fg="gray"
            ).pack()

        # =========================
        # DAILY FORECAST
        # =========================
        daily_text = "5-Day Forecast\n\n"

        added_days = []

        for item in data["list"]:

            day = item["dt_txt"][:10]

            if day not in added_days:

                added_days.append(day)

                temp = item["main"]["temp"]

                condition = item["weather"][0]["description"]

                daily_text += f"{day} → {temp:.1f}°C | {condition}\n"

            if len(added_days) == 5:
                break

        daily_label.config(
            text=daily_text,
            bg=bg_color
        )

    except Exception as e:

        daily_label.config(text=str(e))

# =========================
# UNIT TOGGLE
# =========================
def toggle_unit():

    global unit

    if unit == "metric":

        unit = "imperial"

        unit_btn.config(text="Switch to °C")

    else:

        unit = "metric"

        unit_btn.config(text="Switch to °F")

    # Refresh weather automatically
    if city_entry.get() != "":
        get_weather()

# =========================
# CLEAR FUNCTION
# =========================
def clear():

    city_entry.delete(0, tk.END)

    city_label.config(text="")
    temp_label.config(text="")
    desc_label.config(text="")
    details_label.config(text="")
    daily_label.config(text="")

    for widget in forecast_frame.winfo_children():
        widget.destroy()

    root.configure(bg="#1e272e")
    main_frame.configure(bg="#1e272e")

# =========================
# GUI
# =========================
root = tk.Tk()

root.title("Smart Weather App")

root.geometry("1000x850")

root.configure(bg="#1e272e")

main_frame = tk.Frame(root, bg="#1e272e")

main_frame.pack(fill="both", expand=True)

# =========================
# TITLE
# =========================
title = tk.Label(
    main_frame,
    text="🌦 Smart Weather App",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#1e272e"
)

title.pack(pady=20)

# =========================
# ENTRY
# =========================
city_entry = tk.Entry(
    main_frame,
    font=("Arial", 16),
    justify="center",
    width=25
)

city_entry.pack(pady=10)

# =========================
# BUTTONS
# =========================
btn_frame = tk.Frame(main_frame, bg="#16222A")

btn_frame.pack(pady=15)

tk.Button(
    btn_frame,
    text="Get Weather",
    bg="#2ecc71",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    bd=0,
    padx=15,
    pady=8,
    activebackground="#27ae60",
    activeforeground="white",
    command=get_weather
).grid(row=0, column=0, padx=10)

unit_btn = tk.Button(
    btn_frame,
    text="Switch to °F",
    bg="#3498db",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    bd=0,
    activebackground="#3498db",
    activeforeground="white",
    
    command=toggle_unit
)

unit_btn.grid(row=0, column=1, padx=10)

tk.Button(
    btn_frame,
    text="Clear",
    bg="#e74c3c",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    bd=0,
    activebackground="#e74c3c",
    activeforeground="white",
    
    command=clear
).grid(row=0, column=2, padx=10)

# =========================
# WEATHER DISPLAY
# =========================
city_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#1e272e"
)

city_label.pack(pady=10)

temp_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 42, "bold"),
    fg="white",
    bg="#1e272e"
)

temp_label.pack()

desc_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 18),
    fg="white",
    bg="#1e272e"
)

desc_label.pack(pady=5)

details_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 13),
    fg="white",
    bg="#1e272e",
    justify="left"
)

details_label.pack(pady=15)

# =========================
# FORECAST TITLE
# =========================
forecast_title = tk.Label(
    main_frame,
    text="Hourly Forecast",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#1e272e"
)

forecast_title.pack(pady=8)

# =========================
# FORECAST FRAME
# =========================
forecast_frame = tk.Frame(
    main_frame,
    bg="#1e272e"
)

forecast_frame.pack(pady=5)

# =========================
# DAILY FORECAST
# =========================
daily_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 12),
    fg="white",
    bg="#1e272e",
    justify="left"
)

daily_label.pack(pady=20)

# =========================
# RUN
# =========================
root.mainloop()