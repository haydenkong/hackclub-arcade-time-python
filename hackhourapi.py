import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json

API_KEY = 'YOUR /API KEY HERE'
BASE_URL = 'https://hackhour.hackclub.com'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

def start_session(slack_id, work):
    url = f'{BASE_URL}/api/start/{slack_id}'
    data = {
        'work': work
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def pause_or_resume_session(slack_id):
    url = f'{BASE_URL}/api/pause/{slack_id}'
    response = requests.post(url, headers=headers)
    return response.json()

def cancel_session(slack_id):
    url = f'{BASE_URL}/api/cancel/{slack_id}'
    response = requests.post(url, headers=headers)
    return response.json()

def get_latest_session(slack_id):
    url = f'{BASE_URL}/api/session/{slack_id}'
    response = requests.get(url, headers=headers)
    return response.json()

def get_stats(slack_id):
    url = f'{BASE_URL}/api/stats/{slack_id}'
    response = requests.get(url, headers=headers)
    return response.json()

def get_goals(slack_id):
    url = f'{BASE_URL}/api/goals/{slack_id}'
    response = requests.get(url, headers=headers)
    return response.json()

def get_history(slack_id):
    url = f'{BASE_URL}/api/history/{slack_id}'
    response = requests.get(url, headers=headers)
    return response.json()

def display_json_tree(parent, json_dict, tree):
    for key, value in json_dict.items():
        if isinstance(value, dict):
            node = tree.insert(parent, 'end', text=key, open=True)
            display_json_tree(node, value, tree)
        elif isinstance(value, list):
            node = tree.insert(parent, 'end', text=key, open=True)
            for i, item in enumerate(value):
                item_node = tree.insert(node, 'end', text=f'[{i}]', open=True)
                if isinstance(item, dict):
                    display_json_tree(item_node, item, tree)
                else:
                    tree.insert(item_node, 'end', text=item)
        else:
            tree.insert(parent, 'end', text=f'{key}: {value}')

def display_result(result):
    for i in tree.get_children():
        tree.delete(i)
    display_json_tree('', result, tree)

def start_session_gui():
    work = work_entry.get()
    result = start_session(slack_id, work)
    display_result(result)

def pause_or_resume_session_gui():
    result = pause_or_resume_session(slack_id)
    display_result(result)

def cancel_session_gui():
    result = cancel_session(slack_id)
    display_result(result)

def get_latest_session_gui():
    result = get_latest_session(slack_id)
    display_result(result)

def get_stats_gui():
    result = get_stats(slack_id)
    display_result(result)

def get_goals_gui():
    result = get_goals(slack_id)
    display_result(result)

def get_history_gui():
    result = get_history(slack_id)
    display_result(result)

slack_id = 'YOUR SLACK ID HERE'

root = tk.Tk()
root.title("Session Manager")

frame = tk.Frame(root)
frame.pack(pady=10)

work_label = tk.Label(frame, text="Work Description:")
work_label.grid(row=0, column=0, padx=5, pady=5)
work_entry = tk.Entry(frame, width=40)
work_entry.grid(row=0, column=1, padx=5, pady=5)

start_button = tk.Button(frame, text="Start Session", command=start_session_gui)
start_button.grid(row=1, column=0, columnspan=2, pady=5)

pause_resume_button = tk.Button(frame, text="Pause/Resume Session", command=pause_or_resume_session_gui)
pause_resume_button.grid(row=2, column=0, columnspan=2, pady=5)

cancel_button = tk.Button(frame, text="Cancel Session", command=cancel_session_gui)
cancel_button.grid(row=3, column=0, columnspan=2, pady=5)

latest_button = tk.Button(frame, text="View Latest Session", command=get_latest_session_gui)
latest_button.grid(row=4, column=0, columnspan=2, pady=5)

stats_button = tk.Button(frame, text="View Stats", command=get_stats_gui)
stats_button.grid(row=5, column=0, columnspan=2, pady=5)

goals_button = tk.Button(frame, text="View Goals", command=get_goals_gui)
goals_button.grid(row=6, column=0, columnspan=2, pady=5)

history_button = tk.Button(frame, text="View History", command=get_history_gui)
history_button.grid(row=7, column=0, columnspan=2, pady=5)

exit_button = tk.Button(frame, text="Exit", command=root.quit)
exit_button.grid(row=8, column=0, columnspan=2, pady=5)

tree = ttk.Treeview(root)
tree.pack(pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
