import requests
import json

API_KEY = 'Your /api Key here'
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

def main():
    slack_id = 'Your Slack ID here'
    
    while True:
        print("\nOptions:")
        print("1. Start a new session")
        print("2. Pause/Resume session")
        print("3. Cancel session")
        print("4. View latest session")
        print("5. View stats")
        print("6. View goals")
        print("7. View history")
        print("8. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            work = input("Enter the work description: ")
            result = start_session(slack_id, work)
            print(json.dumps(result, indent=4))
        
        elif choice == '2':
            result = pause_or_resume_session(slack_id)
            print(json.dumps(result, indent=4))
        
        elif choice == '3':
            result = cancel_session(slack_id)
            print(json.dumps(result, indent=4))
        
        elif choice == '4':
            result = get_latest_session(slack_id)
            print(json.dumps(result, indent=4))
        
        elif choice == '5':
            result = get_stats(slack_id)
            print(json.dumps(result, indent=4))
        
        elif choice == '6':
            result = get_goals(slack_id)
            print(json.dumps(result, indent=4))
        
        elif choice == '7':
            result = get_history(slack_id)
            print(json.dumps(result, indent=4))
        
        elif choice == '8':
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
