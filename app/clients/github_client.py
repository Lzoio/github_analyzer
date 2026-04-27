# Github API Calls
import requests
from app.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
} if GITHUB_TOKEN else {}

def get_user(username):
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 404:
        return {"error": "User not found"}
    
    if response.status_code == 403:
        return {"error": "Rate limit exceeded"}
    
    if response.status_code != 200:
        return {"error": "Github API error"}
    
    return response.json()

def get_repos(username):
    all_repos = []
    page = 1

    while True:
        url = f"{BASE_URL}/users/{username}/repos"
        params = {
            "per_page": 100,
            "page": page
        }

        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            return {"error": response.json().get("message", "Error fetching repos")}
        
        repos = response.json()

        if page > 10:
            print("[WARNING] Too many pages, stopping early")
            break

        if not repos: 
            break

        all_repos.extend(repos)
        page += 1

    return all_repos

def get_user_events(username):
    events = []
    page = 1

    while True:
        url = f"{BASE_URL}/users/{username}/events"
        params = {
            "per_page": 100,
            "page": page
        }

        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            return {"error": response.json().get("message", "Error fetching events")}
        
        batch = response.json()

        print(f"[CLIENT] Events page {page}: {len(batch)}")

        if not batch:
            break

        events.extend(batch)
        page += 1

        if page > 3:
            break
    
    print(f"[CLIENT] Total events fetched: {len(events)}")

    return events