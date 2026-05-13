import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox
import emoji

# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()
root.title("Advanced GUI Chat App")
root.geometry("900x750")
root.configure(bg="#0f172a")
main_chat_frame = tk.Frame(root, bg="#0f172a")

current_user = "User 1"
bot_mode = False
username = ""
current_room = "General"

chat_rooms = {
    "General": [],
    "Friends": [],
    "Study": []
}
# =========================
# FUNCTIONS
# =========================

def switch_user():

    global current_user

    if current_user == "User 1":

        current_user = "User 2"

        user_btn.config(
            text="Switch: User 2",
            bg="#8b5cf6"
        )

    else:

        current_user = "User 1"

        user_btn.config(
            text="Switch: User 1",
            bg="#06b6d4"
        )

def bot_reply(message):

    message = message.lower()

    # Greetings
    if "hi" in message or "hello" in message:
        return "Hello 👋 How are you?"

    elif "how are you" in message:
        return "I'm doing great 😊 What about you?"

    elif "fine" in message or "good" in message:
        return "That's nice to hear 😄"

    # Feelings
    elif "sad" in message:
        return "Don't worry ❤️ Better days are coming."

    elif "boring" in message or "bored" in message:
        return "Maybe try listening to music 🎵 or watching a movie 🍿"

    elif "tired" in message:
        return "Take some rest 😴"

    elif "happy" in message:
        return "Yayyy 🎉 Keep smiling 😄"

    # Study
    elif "study" in message or "exam" in message:
        return "You can do it 📚🔥"

    elif "python" in message:
        return "Python is awesome 🐍"

    elif "machine learning" in message or "ml" in message:
        return "ML is one of the coolest technologies 🤖"

    # Personal
    elif "your name" in message:
        return "I'm Smart Chat Bot 🤖"

    elif "college" in message:
        return "College life is full of memories 🎓"

    elif "friend" in message:
        return "Good friends make life better 💙"

    # Fun
    elif "joke" in message:
        return "Why do programmers prefer dark mode? Because light attracts bugs 😂"

    elif "movie" in message:
        return "I love sci-fi movies 🚀"

    elif "music" in message:
        return "Music makes everything better 🎶"

    # Goodbye
    elif "bye" in message:
        return "Goodbye 👋 Have a great day!"

    # Default
    else:
        return "That's interesting 😄 Tell me more."
def toggle_bot():

    global bot_mode

    if bot_mode == False:

        bot_mode = True

        bot_btn.config(
            text="Bot Mode ON",
            bg="#22c55e"
        )

    else:

        bot_mode = False

        bot_btn.config(
            text="Bot Mode OFF",
            bg="#ef4444"
        )
        messagebox.showinfo(
            "Bot Mode",
            "Bot Mode Enabled 🤖"
        )

        messagebox.showinfo(
            "Bot Mode",
            "Bot Mode Disabled ❌"
        )


def login():

    global username

    entered_name = username_entry.get()

    if entered_name.strip() == "":
        return

    username = entered_name

    login_frame.pack_forget()

    main_chat_frame.pack(fill="both", expand=True)


def switch_room(room_name):

    global current_room

    current_room = room_name

    room_label.config(text=f"Room: {room_name}")

    chat_area.delete(1.0, tk.END)

    for message, tag in chat_rooms[room_name]:

        chat_area.insert(tk.END, message, tag)

    chat_area.yview(tk.END)


def send_image():

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:

        current_time = datetime.now().strftime("%I:%M %p")

        chat_area.insert(
            tk.END,
            f"\n📷 {username} sent an image\n{file_path}\n",
            "user1"
        )

        chat_area.yview(tk.END)
        messagebox.showinfo(
    "Image Shared",
    "Image sent successfully 📷"
)









def send_message():

    message = entry_box.get()

    if message.strip() == "":
        return

    time = datetime.now().strftime("%I:%M %p")

    final_message = emoji.emojize(message, language='alias')

    # =========================
    # USER MESSAGE
    # =========================

    if current_user == "User 1":
        chat_area.insert(
        tk.END,
        f"\n{username} [{time}]\n{final_message}\n",
        "user1"
    )
        chat_rooms[current_room].append(
    (
        f"\n{username} [{time}]\n{final_message}\n",
        "user1"
    )
)

    else:
        chat_area.insert(
        tk.END,
        f"\nUser 2 [{time}]\n{final_message}\n",
        "user2"
    )
        chat_rooms[current_room].append(
    (
        f"\nUser 2 [{time}]\n{final_message}\n",
        "user2"
    )
)

    # =========================
    # SAVE CHAT
    # =========================

    with open("chat_history.txt", "a", encoding="utf-8") as file:
        if current_user == "User 1":
            file.write(f"{username} [{time}] : {final_message}\n")
        else:
            file.write(f"User 2 [{time}] : {final_message}\n")
    entry_box.delete(0, tk.END)
    chat_area.yview(tk.END)
    root.title(f"New Message from {current_user}")

    root.after(
    2000,
    lambda: root.title("Advanced GUI Chat App")
)

    # =========================
    # BOT REPLY
    # =========================

    if bot_mode == True and current_user == "User 1":

        bot_message = bot_reply(final_message)

        bot_time = datetime.now().strftime("%I:%M %p")

        chat_area.insert(
            tk.END,
            f"\nBot [{bot_time}]\n{bot_message}\n",
            "user2"
        )

        chat_area.yview(tk.END)


def clear_chat():
    chat_area.delete("1.0", tk.END)

    with open("chat_history.txt", "w", encoding="utf-8") as file:
        file.write("")


# =========================
# LOGIN SCREEN
# =========================

login_frame = tk.Frame(root, bg="#0f172a")
login_frame.pack(fill="both", expand=True)

login_title = tk.Label(
    login_frame,
    text="🔐 Login",
    font=("Arial", 28, "bold"),
    bg="#0f172a",
    fg="white"
)

login_title.pack(pady=40)

username_entry = tk.Entry(
    login_frame,
    font=("Arial", 16),
    width=25,
    justify="center",
    bg="#334155",
    fg="white",
    insertbackground="white"
)

username_entry.pack(pady=20)

login_btn = tk.Button(
    login_frame,
    text="Enter Chat",
    font=("Arial", 14, "bold"),
    bg="#22c55e",
    fg="white",
    padx=20,
    pady=5,
    command=login
)

login_btn.pack(pady=20)





# =========================
# TITLE
# =========================

title = tk.Label(
    root,
    text="💬 Advanced GUI Chat App",
    font=("Segoe UI Emoji", 12),
    bg="#0f172a",
    fg="white"
)

title.pack(pady=15)

title.pack(pady=15)

# =========================
# ROOM TITLE
# =========================

room_label = tk.Label(
    main_chat_frame,
    text="Room: General",
    font=("Arial", 14, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
)

room_label.pack(pady=5)

# =========================
# ROOM BUTTONS
# =========================

room_frame = tk.Frame(main_chat_frame, bg="#0f172a")
room_frame.pack(pady=5)

general_btn = tk.Button(
    room_frame,
    text="General",
    bg="#3b82f6",
    fg="white",
    command=lambda: switch_room("General")
)

general_btn.grid(row=0, column=0, padx=5)

friends_btn = tk.Button(
    room_frame,
    text="Friends",
    bg="#8b5cf6",
    fg="white",
    command=lambda: switch_room("Friends")
)

friends_btn.grid(row=0, column=1, padx=5)

study_btn = tk.Button(
    room_frame,
    text="Study",
    bg="#10b981",
    fg="white",
    command=lambda: switch_room("Study")
)

study_btn.grid(row=0, column=2, padx=5)


# =========================
# CHAT AREA
# =========================

chat_area = scrolledtext.ScrolledText(
    main_chat_frame,
    wrap=tk.WORD,
    font=("Arial", 12),
    bg="#1e293b",
    fg="white",
    width=70,
    height=18,
    bd=0
)

chat_area.pack(padx=20, pady=10)

chat_area.tag_config(
    "user1",
    foreground="#38bdf8",
    spacing1=10,
    spacing3=10
)

chat_area.tag_config(
    "user2",
    foreground="#f472b6",
    spacing1=10,
    spacing3=10
)

# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(main_chat_frame, bg="#0f172a")
input_frame.pack(pady=10)

entry_box = tk.Entry(
    input_frame,
    font=("Arial", 14),
    width=35,
    bg="#334155",
    fg="white",
    insertbackground="white"
)

entry_box.grid(row=0, column=0, padx=10)

send_btn = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 12, "bold"),
    bg="#22c55e",
    fg="white",
    padx=15,
    command=send_message
)

send_btn.grid(row=0, column=1, padx=5)

image_btn = tk.Button(
    input_frame,
    text="Send Image",
    font=("Arial", 11, "bold"),
    bg="#8b5cf6",
    fg="white",
    command=send_image
)

image_btn.grid(row=0, column=2, padx=5)









# =========================
# BOTTOM BUTTONS
# =========================

bottom_frame = tk.Frame(main_chat_frame, bg="#0f172a")
bottom_frame.pack(pady=10)

user_btn = tk.Button(
    bottom_frame,
    text="Switch: User 1",
    font=("Arial", 11, "bold"),
    bg="#06b6d4",
    fg="white",
    padx=15,
    command=switch_user
)

user_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(
    bottom_frame,
    text="Clear Chat",
    font=("Arial", 11, "bold"),
    bg="#ef4444",
    fg="white",
    padx=15,
    command=clear_chat
)

clear_btn.grid(row=0, column=1, padx=10)


bot_btn = tk.Button(
    bottom_frame,
    text="Bot Mode OFF",
    font=("Arial", 11, "bold"),
    bg="#ef4444",
    fg="white",
    padx=15,
    command=toggle_bot
)

bot_btn.grid(row=0, column=2, padx=10)

# =========================
# FOOTER
# =========================

footer = tk.Label(
    main_chat_frame,
    text="Python Tkinter Chat Application",
    font=("Arial", 10),
    bg="#0f172a",
    fg="gray"
)

footer.pack(pady=10)

root.mainloop()