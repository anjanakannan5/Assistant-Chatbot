import re
import long_responses as long
import emoji
from duckduckgo_search import DDGS
import requests
from PIL import Image
from io import BytesIO
import json
import os
import time
import threading
from plyer import notification
import platform
import tkinter as tk
from tkinter import ttk
import datetime
import operator

# Function to manage notes
def manage_notes(username, action, note=None):
    file_name = f"{username}_notes.json"
    # If notes file doesn't exist, create it
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            json.dump([], f)
    # Load existing notes
    with open(file_name, 'r') as f:
        notes = json.load(f)
    # Add a new note
    if action == "add" and note:
        notes.append(note)
        with open(file_name, 'w') as f:
            json.dump(notes, f)
        return "Note added successfully!"
    # View all notes
    elif action == "view":
        return "\n".join(notes) if notes else "No notes found."
    # Delete a note
    elif action == "delete" and note:
        if note in notes:
            notes.remove(note)
            with open(file_name, 'w') as f:
                json.dump(notes, f)
            return "Note deleted successfully!"
        else:
            return "Note not found."

# Sound Function
try:
    import winsound  # Windows
except ImportError:
    from playsound import playsound  # Linux & macOS
def play_notification_sound():
    """Plays a notification sound."""
    sound_path = "notification.wav"  # Replace with your sound file
    if platform.system() == "Windows":
        winsound.PlaySound(sound_path, winsound.SND_FILENAME)
    else:
        playsound(sound_path)  # Linux/macOS

def show_reminder(task):
    """Displays a pop-up reminder with sound."""
    play_notification_sound()  # Play sound when reminder triggers
    popup = tk.Tk()
    popup.title("Reminder!")
    popup.geometry("350x150")
    popup.configure(bg="lightblue")  # lightblue background
    popup.attributes("-topmost", True)  # Keep window on top
    label = tk.Label(popup, text=f"⏰ Reminder: {task}!", font=("Arial", 14, "bold"), bg="lightblue")
    label.pack(pady=20)
    button = tk.Button(popup, text="OK, Got It!", command=popup.destroy)
    button.pack(pady=10)
    popup.mainloop()

def set_monthly_reminder(task, day):
    """Sets a monthly reminder for the specified task and day."""
    try:
        day = int(day)
        if day < 1 or day > 31:
            return "⚠️ Invalid day! Please specify a day between 1 and 31."
        def notify():
            current_day = datetime.datetime.now().day
            if current_day == day:
                tk_root = tk.Tk()
                tk_root.withdraw()  # Hide root window
                show_reminder(task)  # Show the reminder
                tk_root.mainloop()  # Ensure Tkinter runs
        threading.Thread(target=notify, daemon=True).start()
        return f"📅 Monthly reminder for '{task}' set for the {day}th of every month."
    except ValueError:
        return "⚠️ Invalid day! Please specify a valid number between 1 and 31."

def set_reminder(task, delay):
    """Sets a reminder that triggers after 'delay' seconds, with sound."""
    try:
        delay = int(delay)
        if delay <= 0:
            return "⚠️ Time must be positive!"
        def notify():
            time.sleep(delay)
            tk_root = tk.Tk()
            tk_root.withdraw()  # Hide root window
            tk_root.after(0, show_reminder, task)  # Schedule pop-up
            tk_root.mainloop()  # Ensure Tkinter runs
        threading.Thread(target=notify, daemon=True).start()
        return f"⏳ Reminder set for '{task}' in {delay} seconds!"
    except ValueError:
        return "⚠️ Invalid format! Use: set reminder 'task' in X seconds."

# User authentication function
def authenticate_user():
    users_file = "users.json"
    if not os.path.exists(users_file):
        with open(users_file, 'w') as f:
            json.dump({}, f)
    with open(users_file, 'r') as f:
        users = json.load(f)
    while True:
        choice = input("Do you have an account? (yes/no): ").strip().lower()
        if choice == "yes":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username in users and users[username] == password:
                print("Login successful!\n")
                return username
            else:
                print("Invalid username or password. Try again.\n")
        elif choice == "no":
            username = input("Choose a username: ")
            if username in users:
                print("Username already exists. Try a different one.\n")
                continue
            password = input("Choose a password: ")
            users[username] = password
            with open(users_file, 'w') as f:
                json.dump(users, f)
            print("Account created successfully!\n")
            return username
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.\n")
            
# Function to search the web
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
        if results and 'body' in results[0]:
            answer = results[0]['body']
            return (answer[:290] + "... Read more online.") if len(answer) > 300 else answer
        return "I found some information, but couldn't extract a direct answer."
    except Exception:
        return "I'm having trouble finding that. Could you ask differently?"

# Function to search and display an image
def search_and_display_image(query):
    with DDGS() as ddgs:
        results = list(ddgs.images(query, max_results=1))
    if results:
        image_url = results[0]['image']
        print(f"Image URL: {image_url}")
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img.show()
    else:
        return "No images found."

# Function to check message probability
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainity = sum(1 for word in user_message if word in recognised_words)
    has_required_words = all(word in user_message for word in required_words)
    if has_required_words or single_response:
        return int((message_certainity / len(recognised_words)) * 100)
    return 0

# Function to manage to-do list
def manage_to_do_list(username, action, task=None):
    file_name = f"{username}_todo.json"
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            json.dump([], f)
    with open(file_name, 'r') as f:
        tasks = json.load(f)
    if action == "add" and task:
        tasks.append(task)
    elif action == "delete" and task:
        if task in tasks:
            tasks.remove(task)
        else:
            return "Task not found."
    elif action == "view":
        return "\n".join(tasks) if tasks else "No tasks found."
    with open(file_name, 'w') as f:
        json.dump(tasks, f)
    return "Task updated successfully!"

# Function to check all messages
def check_all_messages(username, message):
    highest_prob_list = {}
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Predefined responses
    response(f"Thank you! {emoji.emojize(':folded_hands:')}", ["nice", "helpful"], single_response=True)
    response(f"Aww, that's really sweet! {emoji.emojize(':red_heart:')}", ["i", "love", "you"], required_words=["love", "you"])
    response(f'Hello! {emoji.emojize(":waving_hand:")}', ["hello", "hi", "hey"], single_response=True)
    response("I'm doing fine, and you?", ["how","are","you"], required_words=["how","are","you"])
    response("Helping users like you! How can I assist you today?", ["what","are","you","doing"], required_words=["what","are","you","doing"])
    response(f"Anytime! Let me know if you need anything else {emoji.emojize(':grinning_face:')}", ["thank", "thanks"], single_response=True)
    response(f"Okay {emoji.emojize(':thumbs_up:')}", ["okie", "okay", "ok", "kay", "done"], single_response=True)
    response(f"I think its impossible!",["will", "i", "pass", "my" ,"exams"], required_words=["pass","my","exams"])
    response(long.R_EATING, ["what", "you", "eat"], required_words=["you", "eat"])
    response(long.NAME, ["what", "is", "your", "name"], required_words=["your", "name"])
    response(long.HELP, ["can", "help"], single_response=True, required_words=["help", "can"])
    response(long.EXIT, ["bye", "bubye", "byeee"], single_response=True, required_words=["bye"])
    response("Sure, let me add that note for you.", ["add", "note"], single_response=True)
    response("Here are your notes.", ["view", "notes"], single_response=True)
    response("Let me delete that note for you.", ["delete", "note"], single_response=True)

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    if "image" in message:
        cleaned_query = re.sub(r"^(give|show|find)?\s*(image|photo|picture|pic)\s*(of|for)?\s*", "", " ".join(message), flags=re.IGNORECASE).strip()
        search_and_display_image(cleaned_query)
        return "Image will pop up soon..."
    elif "add task" in " ".join(message):
        task = " ".join(message).replace("add task", "").strip()
        return manage_to_do_list(username, "add", task)
    elif "delete note" in " ".join(message):
        note = " ".join(message).replace("delete note", "").strip()
        return manage_notes(username, "delete", note)
    elif "delete" in message:
        task = " ".join(message).replace("delete", "").strip()
        return manage_to_do_list(username, "delete", task)
    elif "view tasks" in " ".join(message):
        return manage_to_do_list(username, "view")
    elif "set reminder" in " ".join(message):
        parts = " ".join(message).split(" in ")
        if len(parts) == 2:
            task = parts[0].replace("set reminder", "").strip()
            time_part = parts[1].strip().split()  # Split time value and unit
            if len(time_part) == 2 and time_part[1] in ["seconds", "minutes"]:
                delay = int(time_part[0]) * (60 if time_part[1] == "minutes" else 1)  # Convert to seconds
                return set_reminder(task, delay)
            else:
                return emoji.emojize(":warning: Use: set reminder 'task' in X seconds/minutes", language="alias")
        parts = " ".join(message).split(" every ")
        if len(parts) == 2:
            task = parts[0].replace("set reminder", "").strip()
            day = parts[1].strip().replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
            return set_monthly_reminder(task, day)
        return emoji.emojize(":warning: Invalid command! Use:\n🔹 set reminder 'task' in X seconds/minutes\n🔹 set reminder 'task' every Xth", language="alias")
    
        # Check for note-related actions
    elif "add note" in " ".join(message):
        note = " ".join(message).replace("add note", "").strip()
        return manage_notes(username, "add", note)
    
    elif "view notes" in " ".join(message):
        return manage_notes(username, "view")

    elif highest_prob_list[best_match] >= 10:
        return best_match
    return search_web(" ".join(message))

# Login or Register
username = authenticate_user()

print(f"{emoji.emojize(':sparkles:', language='alias')} Welcome to Your Personal Assistant! {emoji.emojize(':sparkles:', language='alias')}\n")
print(f"{emoji.emojize(':pushpin:', language='alias')} To-Do List Commands :\n")
print(f"{emoji.emojize(':memo:', language='alias')} Add a task : add task 'task description'")
print(f"{emoji.emojize(':x:', language='alias')} Delete a task: delete 'task description'")
print(f"{emoji.emojize(':clipboard:', language='alias')} View all tasks: view tasks\n")
print(f"{emoji.emojize(':alarm_clock:', language='alias')} Reminder Feature :")
print(f"{emoji.emojize(':bell:', language='alias')} Set a reminder: set reminder 'task' in X minutes\n")
print(f"{emoji.emojize(':mag:', language='alias')} Ask Anything!")
print(f"{emoji.emojize(':bulb:', language='alias')} General questions? Just type your query normally!")
print(f"{emoji.emojize(':frame_with_picture:',language='alias')}Want an image? Say: show image of 'X'\n")
print(f"{emoji.emojize(':abacus:', language='alias')} Note Commands :")
print(f"{emoji.emojize(':memo:', language='alias')} Add a note: add note 'your note description'")
print(f"{emoji.emojize(':eyes:', language='alias')} View all notes: view notes")
print(f"{emoji.emojize(':wastebasket:', language='alias')} Delete a note: delete note 'note description'\n")
print(f"{emoji.emojize(':speech_balloon:', language='alias')} I'm here to assist you! How can I help today? {emoji.emojize(':blush:', language='alias')}")

while True:
    user_input = input(f"You {emoji.emojize(':bust_in_silhouette:', language='alias')} : ").strip()
    response = check_all_messages(username, re.split(r'\s+|[,;?!.-]\s*', user_input.lower()))
    print(f"Bot  {emoji.emojize(':robot:',language='alias')} :", response)
    if response == long.EXIT:
        break







