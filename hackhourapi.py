import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime, timedelta
import threading
import time

API_KEY = ''  # Initially empty
SLACK_ID = ''  # Initially empty

BASE_URL = 'https://hackhour.hackclub.com'

class SessionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("HackHour API Manager | By Hayden Kong")
        self.root.geometry("900x700")
        self.headers = {'Authorization': f'Bearer {API_KEY}'}
        self.auto_session_active = False
        self.credentials_saved = False  

        self.setup_ui()
        self.load_credentials()  

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
         
        self.setup_api_overview_tab()
        self.setup_credentials_tab() 
        self.setup_session_tab()
        self.setup_stats_tab()
        self.setup_goals_tab()
        self.setup_history_tab()

    def setup_credentials_tab(self):
        credentials_frame = ttk.Frame(self.notebook)
        self.notebook.add(credentials_frame, text="Credentials")

        slack_id_label = ttk.Label(credentials_frame, text="Slack ID:")
        slack_id_label.grid(row=0, column=0, padx=5, pady=5)

        self.slack_id_entry = ttk.Entry(credentials_frame)
        self.slack_id_entry.grid(row=0, column=1, padx=5, pady=5)

        api_key_label = ttk.Label(credentials_frame, text="API Key:")
        api_key_label.grid(row=1, column=0, padx=5, pady=5)

        self.api_key_entry = ttk.Entry(credentials_frame)
        self.api_key_entry.grid(row=1, column=1, padx=5, pady=5)

        save_button = ttk.Button(credentials_frame, text="Save Credentials", command=self.save_credentials)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def setup_api_overview_tab(self):
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="API Overview")

        ttk.Label(overview_frame, text="Hack Hour API Documentation", font=("Arial", 16, "bold")).pack(pady=10)

        api_text = scrolledtext.ScrolledText(overview_frame, wrap=tk.WORD, width=80, height=20)
        api_text.pack(padx=10, pady=10, expand=True, fill="both")

        api_docs = """
        Hack Hour API Overview:

        Authenticated Endpoints (require 'Authorization: Bearer <apikey>' header):
        1. GET /api/session/:slackId - Get latest session for user
        2. GET /api/stats/:slackId - Get stats for user
        3. GET /api/goals/:slackId - Get goals for user
        4. GET /api/history/:slackId - Get history for user
        5. POST /api/start/:slackId - Start a new session
        6. POST /api/pause/:slackId - Pause/resume current session
        7. POST /api/cancel/:slackId - Cancel current session

        Non-Authenticated Endpoints:
        1. GET /ping - Check if service is alive
        2. GET /status - Get details on hack hour status
        3. GET /api/clock/:slackId - Get expected end time (Deprecated)

        Note: There is no guarantee for the reliability of the API. Use at your own risk. (from official Hack Hour docs)
        """
        api_text.insert(tk.END, api_docs)
        api_text.config(state=tk.DISABLED)

    def setup_session_tab(self):
        session_frame = ttk.Frame(self.notebook)
        self.notebook.add(session_frame, text="Session")

        ttk.Button(session_frame, text="Update latest session stats", command=self.get_latest_session_gui).pack(pady=5)

        work_frame = ttk.Frame(session_frame)
        work_frame.pack(pady=5)
        ttk.Label(work_frame, text="Work:").pack(side=tk.LEFT)
        self.work_entry = ttk.Entry(work_frame, width=40)
        self.work_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(work_frame, text="Start New Session", command=self.start_session_gui).pack(side=tk.LEFT)

        ttk.Button(session_frame, text="Pause/Resume Session", command=self.pause_or_resume_session_gui).pack(pady=5)
        ttk.Button(session_frame, text="Cancel Session", command=self.cancel_session_gui).pack(pady=5)

        auto_session_frame = ttk.Frame(session_frame)
        auto_session_frame.pack(pady=5)
        ttk.Label(auto_session_frame, text="Auto-Session Hours:").pack(side=tk.LEFT)
        self.auto_session_hours = ttk.Entry(auto_session_frame, width=5)
        self.auto_session_hours.pack(side=tk.LEFT, padx=5)
        self.auto_session_button = ttk.Button(auto_session_frame, text="Start Auto-Session",
                                              command=self.start_auto_session)
        self.auto_session_button.pack(side=tk.LEFT)

        self.session_result = scrolledtext.ScrolledText(session_frame, wrap=tk.WORD, width=80, height=20)
        self.session_result.pack(padx=10, pady=10, expand=True, fill="both")

    def setup_stats_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Stats")

        ttk.Button(stats_frame, text="Update Stats", command=self.get_stats_gui).pack(pady=10)

        self.stats_result = scrolledtext.ScrolledText(stats_frame, wrap=tk.WORD, width=80, height=20)
        self.stats_result.pack(padx=10, pady=10, expand=True, fill="both")

    def setup_goals_tab(self):
        goals_frame = ttk.Frame(self.notebook)
        self.notebook.add(goals_frame, text="Goals")

        ttk.Button(goals_frame, text="Update Goals", command=self.get_goals_gui).pack(pady=10)

        self.goals_result = scrolledtext.ScrolledText(goals_frame, wrap=tk.WORD, width=80, height=20)
        self.goals_result.pack(padx=10, pady=10, expand=True, fill="both")

    def setup_history_tab(self):
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="History")

        ttk.Button(history_frame, text="Update History", command=self.get_history_gui).pack(pady=10)

        self.history_result = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, width=80, height=20)
        self.history_result.pack(padx=10, pady=10, expand=True, fill="both")

    def save_credentials(self):
        global API_KEY, SLACK_ID
        API_KEY = self.api_key_entry.get()
        SLACK_ID = self.slack_id_entry.get()
        self.headers = {'Authorization': f'Bearer {API_KEY}'}
        self.root.title("HackHour API Manager | By Hayden Kong" + " | Slack ID: " + SLACK_ID)
        messagebox.showinfo("Credentials Saved", "Your Slack ID and API Key have been saved!")
        self.credentials_saved = True 

        with open("credentials.txt", "w") as f:
            json.dump({"API_KEY": API_KEY, "SLACK_ID": SLACK_ID}, f)

        self.update_all_api_data() 

    def load_credentials(self):
        global API_KEY, SLACK_ID
        try:
            with open("credentials.txt", "r") as f:
                credentials = json.load(f)
                API_KEY = credentials.get("API_KEY", "")
                SLACK_ID = credentials.get("SLACK_ID", "")
                self.slack_id_entry.insert(0, SLACK_ID)
                self.api_key_entry.insert(0, API_KEY)
                self.headers = {'Authorization': f'Bearer {API_KEY}'}
                self.root.title("HackHour API Manager | By Hayden Kong" + " | Slack ID: " + SLACK_ID)
                self.credentials_saved = True  
        except FileNotFoundError:
            pass  

    def api_request(self, endpoint, method='get', data=None):
        if self.credentials_saved:  
            url = f'{BASE_URL}/api/{endpoint}'
            try:
                response = getattr(requests, method)(url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"API request failed: {e}")
                return {"ok": False, "error": str(e)}
        else:
            messagebox.showwarning("Credentials Required",
                                   "Please enter and save your Slack ID and API Key in the Credentials tab first.")
            return {"ok": False, "error": "Credentials not provided."}

    def display_result(self, result, widget, formatter):
        widget.config(state=tk.NORMAL)
        widget.delete('1.0', tk.END)
        formatted_result = formatter(result)
        widget.insert(tk.END, formatted_result)
        widget.config(state=tk.DISABLED)

    def format_session(self, data):
        if not data.get('ok'):
            return f"Error: Failed to retrieve session data. {data.get('error', '')}"

        session = data.get('data', {})
        if not session:
            return "No active session found."

        formatted = f"Session Information:\n\n"
        formatted += f"ID: {session.get('id', 'N/A')}\n"
        formatted += f"Created At: {self.format_datetime(session.get('createdAt', ''))}\n"
        formatted += f"Time: {session.get('time', 'N/A')} minutes\n"
        formatted += f"Elapsed: {session.get('elapsed', 'N/A')} minutes\n"
        formatted += f"Remaining: {session.get('remaining', 'N/A')} minutes\n"
        formatted += f"End Time: {self.format_datetime(session.get('endTime', ''))}\n"
        formatted += f"Goal: {session.get('goal', 'N/A')}\n"
        formatted += f"Status: {'Paused' if session.get('paused') else 'Active'}\n"
        formatted += f"Completed: {'Yes' if session.get('completed') else 'No'}\n"
        return formatted

    def format_stats(self, data):
        if not data.get('ok'):
            return f"Error: Failed to retrieve stats data. {data.get('error', '')}"

        stats = data.get('data', {})
        formatted = f"User Statistics:\n\n"
        formatted += f"Total Sessions: {stats.get('sessions', 'N/A')}\n"
        formatted += f"Total Time: {stats.get('total', 'N/A')} minutes\n"
        return formatted

    def format_goals(self, data):
        if not data.get('ok'):
            return f"Error: Failed to retrieve goals data. {data.get('error', '')}"

        goals = data.get('data', [])
        formatted = f"User Goals:\n\n"
        if not goals:
            formatted += "No goals found.\n"
        else:
            for goal in goals:
                formatted += f"Name: {goal.get('name', 'N/A')}\n"
                formatted += f"Minutes: {goal.get('minutes', 'N/A')}\n\n"
        return formatted

    def format_history(self, data):
        if not data.get('ok'):
            return f"Error: Failed to retrieve history data. {data.get('error', '')}"

        history = data.get('data', [])
        formatted = f"Session History:\n\n"
        if not history:
            formatted += "No session history found.\n"
        else:
            for session in history:
                formatted += f"Created At: {self.format_datetime(session.get('createdAt', ''))}\n"
                formatted += f"Time: {session.get('time', 'N/A')} minutes\n"
                formatted += f"Elapsed: {session.get('elapsed', 'N/A')} minutes\n"
                formatted += f"Goal: {session.get('goal', 'N/A')}\n"
                formatted += f"Ended: {'Yes' if session.get('ended') else 'No'}\n"
                formatted += f"Work: {session.get('work', 'N/A')}\n\n"
        return formatted

    def format_datetime(self, dt_string):
        if not dt_string:
            return "N/A"
        try:
            dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return "Invalid datetime"

    def get_latest_session_gui(self):
        result = self.api_request(f'session/{SLACK_ID}')
        self.display_result(result, self.session_result, self.format_session)

    def start_session_gui(self):
        work = self.work_entry.get()
        if work:
            result = self.api_request(f'start/{SLACK_ID}', method='post', data={'work': work})
            self.display_result(result, self.session_result, self.format_session)
        else:
            messagebox.showwarning("Input Required", "Please enter what you're working on.")

    def pause_or_resume_session_gui(self):
        result = self.api_request(f'pause/{SLACK_ID}', method='post')
        self.display_result(result, self.session_result, self.format_session)

    def cancel_session_gui(self):
        result = self.api_request(f'cancel/{SLACK_ID}', method='post')
        self.display_result(result, self.session_result, self.format_session)

    def get_stats_gui(self):
        result = self.api_request(f'stats/{SLACK_ID}')
        self.display_result(result, self.stats_result, self.format_stats)

    def get_goals_gui(self):
        result = self.api_request(f'goals/{SLACK_ID}')
        self.display_result(result, self.goals_result, self.format_goals)

    def get_history_gui(self):
        result = self.api_request(f'history/{SLACK_ID}')
        self.display_result(result, self.history_result, self.format_history)

    def start_auto_session(self):
        if self.auto_session_active:
            self.auto_session_active = False
            self.auto_session_button.config(text="Start Auto-Session")
            messagebox.showinfo("Auto-Session", "Auto-Session stopped.")
        else:
            try:
                hours = int(self.auto_session_hours.get())
                if hours <= 0:
                    raise ValueError("Hours must be a positive integer.")
                self.auto_session_active = True
                self.auto_session_button.config(text="Stop Auto-Session")
                threading.Thread(target=self.run_auto_session, args=(hours,), daemon=True).start()
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))

    def run_auto_session(self, hours):
        for _ in range(hours):
            if not self.auto_session_active:
                break
            self.start_session_gui()
            for remaining_minutes in range(60, 0, -1):
                if remaining_minutes == 5:
                    messagebox.showinfo("Session Reminder", "5 minutes left. Please submit proof of your session.")
                time.sleep(60)
            time.sleep(60)  
        self.auto_session_active = False
        self.auto_session_button.config(text="Start Auto-Session")
        messagebox.showinfo("Auto-Session", "Auto-Session completed.")

    def update_all_api_data(self):
        if self.credentials_saved:
            self.get_latest_session_gui()
            self.get_stats_gui()
            self.get_goals_gui()
            self.get_history_gui()

if __name__ == "__main__":
    root = tk.Tk()
    app = SessionManager(root)
    root.mainloop()