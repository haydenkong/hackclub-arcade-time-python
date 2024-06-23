import tkinter as tk
from tkinter import messagebox
import json
import datetime

# Data management class
class HoursTicketsManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {'hours': 0, 'goal': 0}
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

    def undo_hours(self, hours):
        if self.data['hours'] >= hours:
            self.data['hours'] -= hours
            self.save_data()
        else:
            messagebox.showwarning("Invalid Operation", "Cannot undo more hours than logged.")

# GUI application
class ArcadeManagerApp:
    def __init__(self, root):
        self.manager = HoursTicketsManager()
        
        self.root = root
        self.root.title("Hack Club Arcade Manager")
        
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
        
        # Progress bar
        self.progress_frame = tk.Frame(root)
        self.progress_frame.pack(pady=10)
        
        self.progress_canvas = tk.Canvas(self.progress_frame, width=400, height=30, bg='white')
        self.progress_canvas.pack()
        
        # Widget for remaining time
        self.remaining_time_label = tk.Label(root, text=f"Days until end: {self.get_remaining_days()}")
        self.remaining_time_label.pack(pady=10)

        self.update_progress()

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
        remaining_days = self.get_remaining_days()
        days_passed = 5 + (datetime.datetime.now() - datetime.datetime(2024, 6, 18)).days
        total_days = (datetime.datetime(2024, 8, 31) - datetime.datetime(2024, 6, 18)).days
        target_hours = (days_passed / total_days) * goal if goal > 0 else 0
        
        progress_width = 400
        target_width = min(progress_width, int((target_hours / goal) * progress_width)) if goal > 0 else 0
        current_width = min(progress_width, int((hours / goal) * progress_width)) if goal > 0 else 0
        
        self.progress_canvas.create_rectangle(0, 0, target_width, 30, fill='lightblue', outline='black')
        self.progress_canvas.create_rectangle(0, 0, current_width, 30, fill='green', outline='black')

    def get_remaining_days(self):
        end_date = datetime.datetime(2024, 8, 31)
        today = datetime.datetime.now()
        remaining_days = (end_date - today).days
        return remaining_days

if __name__ == "__main__":
    root = tk.Tk()
    app = ArcadeManagerApp(root)
    root.mainloop()
