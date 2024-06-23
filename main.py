

import tkinter as tk
from tkinter import messagebox
import json
import datetime
import requests

class HoursTicketsManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {'hours': 0, 'goal': 0, 'slack_user_id': ''}
            self.save_data()

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def log_hours(self, hours):
        self.data['hours'] += hours
        self.save_data()

    def get_hours(self):
        return self.data['hours']

    def set_goal(self, goal):
        self.data['goal'] = goal
        self.save_data()

    def get_goal(self):
        return self.data.get('goal', 0)

    def set_slack_user_id(self, slack_user_id):
        self.data['slack_user_id'] = slack_user_id
        self.save_data()

    def get_slack_user_id(self):
        return self.data.get('slack_user_id', '')

    def undo_hours(self, hours):
        if self.data['hours'] >= hours:
            self.data['hours'] -= hours
            self.save_data()
        else:
            messagebox.showwarning("Invalid Operation", "Cannot undo more hours than logged.")

class ArcadeManagerApp:
    def __init__(self, root):
        self.manager = HoursTicketsManager()
        
        self.root = root
        self.root.title("Hack Club Arcade Manager")
        
        # Slack User ID input
        self.slack_frame = tk.Frame(root)
        self.slack_frame.pack(pady=10)
        
        self.slack_label = tk.Label(self.slack_frame, text="Enter your Slack User ID:")
        self.slack_label.pack(side=tk.LEFT)
        
        self.slack_entry = tk.Entry(self.slack_frame)
        self.slack_entry.pack(side=tk.LEFT, padx=5)
        self.slack_entry.insert(0, self.manager.get_slack_user_id())
        
        self.slack_button = tk.Button(self.slack_frame, text="Set Slack ID", command=self.set_slack_id)
        self.slack_button.pack(side=tk.LEFT)
        
        # Widgets for logging hours
        self.log_frame = tk.Frame(root)
        self.log_frame.pack(pady=10)
        
        self.log_button = tk.Button(self.log_frame, text="I hacked for an hour", command=self.log_hour)
        self.log_button.pack(side=tk.LEFT, padx=5)
        
        self.undo_button = tk.Button(self.log_frame, text="Oops, I pressed it by mistake", command=self.undo_hour)
        self.undo_button.pack(side=tk.LEFT, padx=5)
        
        # Widgets for setting goal
        self.goal_frame = tk.Frame(root)
        self.goal_frame.pack(pady=10)
        
        self.goal_label = tk.Label(self.goal_frame, text="Set your ticket goal:")
        self.goal_label.pack(side=tk.LEFT)
        
        self.goal_entry = tk.Entry(self.goal_frame)
        self.goal_entry.pack(side=tk.LEFT, padx=5)
        
        self.set_goal_button = tk.Button(self.goal_frame, text="Set Goal", command=self.set_goal)
        self.set_goal_button.pack(side=tk.LEFT)
        
        self.goal_info_label = tk.Label(root, text=f"Ticket Goal: {self.manager.get_goal()}")
        self.goal_info_label.pack(pady=10)
        
        # Progress bars and stats
        self.progress_frame = tk.Frame(root)
        self.progress_frame.pack(pady=10)
        
        self.progress_canvas = tk.Canvas(self.progress_frame, width=400, height=70, bg='white')
        self.progress_canvas.pack()

        # Stats display
        self.stats_frame = tk.Frame(root)
        self.stats_frame.pack(pady=10)

        self.tickets_needed_label = tk.Label(self.stats_frame, text="Tickets needed: ")
        self.tickets_needed_label.pack()

        self.current_percentage_label = tk.Label(self.stats_frame, text="Current percentage: ")
        self.current_percentage_label.pack()

        self.target_percentage_label = tk.Label(self.stats_frame, text="Target percentage: ")
        self.target_percentage_label.pack()

        self.time_left_label = tk.Label(root, text="Minutes left in hour: Not in session")
        self.time_left_label.pack(pady=10)

        self.update_progress()
        self.update_time_left()

    def set_slack_id(self):
        slack_id = self.slack_entry.get()
        self.manager.set_slack_user_id(slack_id)
        messagebox.showinfo("Success", f"Slack User ID set to: {slack_id}")

    def log_hour(self):
        self.manager.log_hours(1)
        self.update_progress()

    def undo_hour(self):
        self.manager.undo_hours(1)
        self.update_progress()

    def set_goal(self):
        try:
            goal = int(self.goal_entry.get())
            self.manager.set_goal(goal)
            self.goal_info_label.config(text=f"Ticket Goal: {self.manager.get_goal()}")
            self.goal_entry.delete(0, tk.END)
            self.update_progress()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid goal.")

    def update_progress(self):
        self.progress_canvas.delete("all")
        goal = self.manager.get_goal()
        hours = self.manager.get_hours()
        
        # Calculate the number of days passed since the start date
        start_date = datetime.datetime(2024, 6, 18)
        end_date = datetime.datetime(2024, 8, 31)
        today = datetime.datetime.now()
        
        days_passed = (today - start_date).days
        total_days = (end_date - start_date).days
        
        # Ensure days_passed is at least 1 to avoid division by zero
        days_passed = max(days_passed, 1)

        # Calculate target hours based on the goal and elapsed days
        target_hours = (days_passed / total_days) * goal if goal > 0 else 0
        
        # Determine the width of the progress bars
        progress_width = 400
        target_width = min(progress_width, int((target_hours / goal) * progress_width)) if goal > 0 else 0
        current_width = min(progress_width, int((hours / goal) * progress_width)) if goal > 0 else 0
        
        # Draw the progress bars
        self.progress_canvas.create_rectangle(0, 0, target_width, 30, fill='lightblue', outline='black')
        self.progress_canvas.create_text(10, 15, anchor='w', text="You should be here")
        self.progress_canvas.create_rectangle(0, 40, current_width, 70, fill='green', outline='black')
        self.progress_canvas.create_text(10, 55, anchor='w', text="You are here")

        # Update stats
        tickets_needed = max(0, goal - hours)
        current_percentage = (hours / goal) * 100 if goal > 0 else 0
        target_percentage = (target_hours / goal) * 100 if goal > 0 else 0

        self.tickets_needed_label.config(text=f"Tickets needed: {tickets_needed:.1f}")
        self.current_percentage_label.config(text=f"Current percentage: {current_percentage:.1f}%")
        self.target_percentage_label.config(text=f"Target percentage: {target_percentage:.1f}%")

    def get_time_left(self):
        slack_id = self.manager.get_slack_user_id()
        if not slack_id:
            return -1
        try:
            response = requests.get(f"https://hackhour.hackclub.com/api/clock/{slack_id}")
            time_left = response.json()
            return time_left
        except requests.RequestException:
            return -1

    def update_time_left(self):
        time_left = self.get_time_left()
        if time_left == -1:
            self.time_left_label.config(text="Minutes left in hour: Not in session")
        else:
            minutes_left = time_left // (1000 * 60)  # Convert milliseconds to minutes
            self.time_left_label.config(text=f"Minutes left in hour: {minutes_left}")
        
        # Schedule the next update in 30 seconds
        self.root.after(30000, self.update_time_left)

if __name__ == "__main__":
    root = tk.Tk()
    app = ArcadeManagerApp(root)
    root.mainloop()