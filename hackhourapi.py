import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json

API_KEY = 'YOUR /API KEY HERE'
BASE_URL = 'https://hackhour.hackclub.com'
SLACK_ID = 'YOUR SLACK ID HERE'

class SessionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("HackHour API Manager")
        self.root.geometry("800x600")
        self.headers = {'Authorization': f'Bearer {API_KEY}'}
        
        self.setup_ui()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.setup_api_overview_tab()
        self.setup_session_tab()
        self.setup_stats_tab()
        self.setup_goals_tab()
        self.setup_history_tab()

    def setup_api_overview_tab(self):
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="API Overview")

        ttk.Label(overview_frame, text="HackHour API Documentation", font=("Arial", 16, "bold")).pack(pady=10)

        api_text = scrolledtext.ScrolledText(overview_frame, wrap=tk.WORD, width=80, height=20)
        api_text.pack(padx=10, pady=10, expand=True, fill="both")
        
        api_docs = """
        HackHour API Overview:

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

        Note: There is no guarantee for the reliability of the API. Use at your own risk.
        """
        api_text.insert(tk.END, api_docs)
        api_text.config(state=tk.DISABLED)

    def setup_session_tab(self):
        session_frame = ttk.Frame(self.notebook)
        self.notebook.add(session_frame, text="Session")

        ttk.Button(session_frame, text="Get Latest Session", command=self.get_latest_session_gui).pack(pady=5)
        ttk.Button(session_frame, text="Start New Session", command=self.start_session_gui).pack(pady=5)
        ttk.Button(session_frame, text="Pause/Resume Session", command=self.pause_or_resume_session_gui).pack(pady=5)
        ttk.Button(session_frame, text="Cancel Session", command=self.cancel_session_gui).pack(pady=5)

        self.session_result = scrolledtext.ScrolledText(session_frame, wrap=tk.WORD, width=70, height=15)
        self.session_result.pack(padx=10, pady=10, expand=True, fill="both")

    def setup_stats_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Stats")

        ttk.Button(stats_frame, text="Get Stats", command=self.get_stats_gui).pack(pady=10)

        self.stats_result = scrolledtext.ScrolledText(stats_frame, wrap=tk.WORD, width=70, height=15)
        self.stats_result.pack(padx=10, pady=10, expand=True, fill="both")

    def setup_goals_tab(self):
        goals_frame = ttk.Frame(self.notebook)
        self.notebook.add(goals_frame, text="Goals")

        ttk.Button(goals_frame, text="Get Goals", command=self.get_goals_gui).pack(pady=10)

        self.goals_result = scrolledtext.ScrolledText(goals_frame, wrap=tk.WORD, width=70, height=15)
        self.goals_result.pack(padx=10, pady=10, expand=True, fill="both")

    def setup_history_tab(self):
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="History")

        ttk.Button(history_frame, text="Get History", command=self.get_history_gui).pack(pady=10)

        self.history_result = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, width=70, height=15)
        self.history_result.pack(padx=10, pady=10, expand=True, fill="both")

    def api_request(self, endpoint, method='get', data=None):
        url = f'{BASE_URL}/api/{endpoint}'
        response = getattr(requests, method)(url, headers=self.headers, json=data)
        return response.json()

    def display_result(self, result, widget):
        widget.config(state=tk.NORMAL)
        widget.delete('1.0', tk.END)
        widget.insert(tk.END, json.dumps(result, indent=2))
        widget.config(state=tk.DISABLED)

    def get_latest_session_gui(self):
        result = self.api_request(f'session/{SLACK_ID}')
        self.display_result(result, self.session_result)

    def start_session_gui(self):
        work = tk.simpledialog.askstring("Input", "What are you working on?")
        if work:
            result = self.api_request(f'start/{SLACK_ID}', method='post', data={'work': work})
            self.display_result(result, self.session_result)

    def pause_or_resume_session_gui(self):
        result = self.api_request(f'pause/{SLACK_ID}', method='post')
        self.display_result(result, self.session_result)

    def cancel_session_gui(self):
        result = self.api_request(f'cancel/{SLACK_ID}', method='post')
        self.display_result(result, self.session_result)

    def get_stats_gui(self):
        result = self.api_request(f'stats/{SLACK_ID}')
        self.display_result(result, self.stats_result)

    def get_goals_gui(self):
        result = self.api_request(f'goals/{SLACK_ID}')
        self.display_result(result, self.goals_result)

    def get_history_gui(self):
        result = self.api_request(f'history/{SLACK_ID}')
        self.display_result(result, self.history_result)

if __name__ == "__main__":
    root = tk.Tk()
    app = SessionManager(root)
    root.mainloop()