import requests
import re

url = "https://ocdb.cc/episodes/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Encoding": "identity"  # Forces uncompressed response
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    response.encoding = 'utf-8'
    content = response.text

    # Regular expression to match the episode URLs
    pattern = r"https://ocdb\.cc/episode/[\w-]+-v-[\w-]+/"

    # Find all matching URLs
    episode_urls = re.findall(pattern, content)
else:
    print(f"Failed to retrieve page: {response.status_code}")

print(episode_urls)