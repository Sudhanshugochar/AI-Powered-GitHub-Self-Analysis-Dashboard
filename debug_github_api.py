import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
username = os.getenv("GITHUB_USERNAME", "Sudhanshugochar")

print(f"Checking GitHub API for user: {username}")
print(f"Token present: {'Yes' if token else 'No'}")

headers = {}
if token:
    headers["Authorization"] = f"token {token}"

def check_rate_limit():
    url = "https://api.github.com/rate_limit"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            core = data["resources"]["core"]
            print(f"Rate Limit Config: Limit={core['limit']}, Remaining={core['remaining']}")
            print(f"Reset Time (epoch): {core['reset']}")
            import time
            print(f"Reset Time (local): {time.ctime(core['reset'])}")
        else:
            print(f"Error checking rate limit: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception checking rate limit: {e}")

check_rate_limit()

# explicit fetch to see actual response
if username:
    url = f"https://api.github.com/users/{username}"
    print(f"\nFetching profile: {url}")
    resp = requests.get(url, headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
