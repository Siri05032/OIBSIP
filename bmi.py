from tkinter import *
import csv
import os
import matplotlib.pyplot as plt

# ---------------- BMI CALCULATION ----------------
def calculate_bmi():
    try:
        name = name_entry.get()
        age = age_entry.get()
        gender = gender_var.get()
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if name == "" or age == "":
            result_label.config(text="Enter all details", fg="red")
            return

        bmi = weight / (height * height)
        bmi = round(bmi, 2)

        result_label.config(text="BMI: " + str(bmi), fg="black")

        if bmi < 18.5:
            category = "Underweight"
            suggestion = "Eat more nutritious food"
            color = "blue"
        elif bmi < 25:
            category = "Normal"
            suggestion = "Maintain your lifestyle"
            color = "green"
        elif bmi < 30:
            category = "Overweight"
            suggestion = "Exercise regularly"
            color = "orange"
        else:
            category = "Obese"
            suggestion = "Consult a doctor"
            color = "red"

        category_label.config(text="Category: " + category, fg=color)
        suggestion_label.config(text="Suggestion: " + suggestion)


        # Health Score
        if bmi < 18.5:
            score = 60
        elif bmi < 25:
            score = 95
        elif bmi < 30:
            score = 75
        else:
            score = 50
        score_label.config(text="Health Score: " + str(score) + "/100")


        # Save to CSV
        file_exists = os.path.isfile("bmi_data.csv")

        with open("bmi_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name","Age","Gender","Height","Weight","BMI","Category"])
            writer.writerow([name, age, gender, height, weight, bmi, category])

    except:
        result_label.config(text="Invalid Input", fg="red")




#--------------history_graph---------------------------
def show_history_graph():
    try:
        import matplotlib.pyplot as plt

        bmi_values = []

        if os.path.exists("bmi_data.csv"):
            with open("bmi_data.csv", "r") as file:
                next(file)  # skip header
                for row in file:
                    data = row.strip().split(",")
                    bmi_values.append(float(data[5]))

        if len(bmi_values) == 0:
            result_label.config(text="No history data", fg="red")
            return

        plt.figure(figsize=(6,4))

        plt.plot(bmi_values, marker='o')

        plt.title("BMI Trend Over Time")
        plt.xlabel("Record Number")
        plt.ylabel("BMI Value")

        plt.grid(True)
        plt.show()

    except:
        result_label.config(text="Error loading history graph", fg="red")



# ---------------- VIEW HISTORY ----------------
def view_history():
    history_window = Toplevel(root)
    history_window.title("User History")
    history_window.geometry("650x350")

    text_area = Text(history_window)
    text_area.pack(fill=BOTH, expand=True)

    if os.path.exists("bmi_data.csv"):
        with open("bmi_data.csv", "r") as file:
            for line in file:
                text_area.insert(END, line)
    else:
        text_area.insert(END, "No data available")


# ---------------- CLEAR HISTORY ----------------
def clear_history():
    if os.path.exists("bmi_data.csv"):
        with open("bmi_data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name","Age","Gender","Height","Weight","BMI","Category"])


# ---------------- RESET FIELDS ----------------
def reset_fields():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    height_entry.delete(0, END)
    weight_entry.delete(0, END)

    result_label.config(text="")
    category_label.config(text="")
    suggestion_label.config(text="")


# ---------------- GRAPH ----------------
def show_graph():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        bmi = weight / (height * height)
        bmi = round(bmi, 2)

        plt.figure(figsize=(6,4))

        # Zones
        plt.axhspan(0, 18.5, color='#ADD8E6', label='Underweight')
        plt.axhspan(18.5, 25, color='#90EE90', label='Normal')
        plt.axhspan(25, 30, color='#FFA500', label='Overweight')
        plt.axhspan(30, 40, color='#FF6347', label='Obese')

        # Your BMI marker
        plt.axhline(bmi, color='black', linewidth=2)
        plt.text(0.1, bmi + 0.5, "Your BMI: " + str(bmi), fontsize=10)

        # Labels
        plt.title("BMI Health Status")
        plt.ylabel("BMI Value")

        # Add ticks (important improvement)
        plt.yticks(range(0, 41, 5))

        plt.legend(loc="upper right")
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        plt.show()

    except:
        result_label.config(text="Enter valid input", fg="red")
# ---------------- GUI ----------------
root = Tk()
root.title("Smart Health Analyzer")
root.geometry("500x600")
root.config(bg="#1e1e2f")   # dark background

# Main container (card style)
main_frame = Frame(root, bg="#2c2f4a", bd=0)
main_frame.pack(pady=30, padx=30, fill="both", expand=True)

# Title
Label(main_frame, text="Smart BMI Analyzer",
      font=("Segoe UI", 20, "bold"),
      bg="#2c2f4a", fg="white").grid(row=0, columnspan=2, pady=15)

# Input labels style
def label_style(text, row):
    Label(main_frame, text=text,
          font=("Segoe UI", 10),
          bg="#2c2f4a", fg="#cfd3ff").grid(row=row, column=0, sticky="w", pady=6)

def entry_style(row):
    e = Entry(main_frame, font=("Segoe UI", 10), bd=0, relief="flat")
    e.grid(row=row, column=1, pady=6, ipady=4, ipadx=6)
    return e

# Inputs
label_style("Name", 1)
name_entry = entry_style(1)

label_style("Age", 2)
age_entry = entry_style(2)

label_style("Gender", 3)
gender_var = StringVar(value="Male")

gender_frame = Frame(main_frame, bg="#2c2f4a")
gender_frame.grid(row=3, column=1)

Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male",
            bg="#2c2f4a", fg="white", selectcolor="#2c2f4a").pack(side=LEFT)
Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female",
            bg="#2c2f4a", fg="white", selectcolor="#2c2f4a").pack(side=LEFT)

label_style("Height (m)", 4)
height_entry = entry_style(4)

label_style("Weight (kg)", 5)
weight_entry = entry_style(5)

# Button style
def btn(text, cmd, color, r, c):
    Button(main_frame, text=text, command=cmd,
           bg=color, fg="white",
           font=("Segoe UI", 10, "bold"),
           activebackground=color,
           relief="flat", width=18).grid(row=r, column=c, padx=6, pady=8)

# Buttons
btn("Calculate BMI", calculate_bmi, "#4CAF50", 6, 0)
btn("Show Graph", show_graph, "#9C27B0", 6, 1)

btn("View History", view_history, "#2196F3", 7, 0)
btn("Reset", reset_fields, "#f44336", 7, 1)

btn("History Graph", show_history_graph, "#673AB7", 8, 0)
btn("Clear History", clear_history, "#795548", 8, 1)

# Result Section
result_frame = Frame(main_frame, bg="#2c2f4a")
result_frame.grid(row=9, columnspan=2, pady=20)

result_label = Label(result_frame, text="", font=("Segoe UI", 12), bg="#2c2f4a", fg="white")
result_label.pack()

category_label = Label(result_frame, text="", font=("Segoe UI", 13, "bold"), bg="#2c2f4a")
category_label.pack()

suggestion_label = Label(result_frame, text="", font=("Segoe UI", 10), bg="#2c2f4a", fg="#cfd3ff")
suggestion_label.pack()

score_label = Label(result_frame, text="", font=("Segoe UI", 11, "bold"), bg="#2c2f4a", fg="#ffd700")
score_label.pack()

root.mainloop()