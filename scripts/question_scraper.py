import requests
import re
from tqdm import tqdm
import time
import csv

url = "https://ocdb.cc/episodes/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Encoding": "identity"  # Forces uncompressed response
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    response.encoding = 'utf-8'
    content = response.text

    print('content = ', content)

    # Regular expression to match the episode URLs
    pattern = r"https://ocdb\.cc/episode/[\w-]+-v-[\w-]+/"

    # Find all matching URLs
    episode_urls = re.findall(pattern, content)
else:
    print(f"Failed to retrieve page: {response.status_code}")


def extract_puzzle_data(episode_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Encoding": "identity"  # Forces uncompressed response
    }

    try:
        ep_response = requests.get(episode_url, headers=headers)
        ep_response.encoding = 'utf-8'  # Ensure correct encoding

        if ep_response.status_code == 200:
            episode_content = ep_response.text

            # 🔍 Find all category blocks (each category with its puzzles)
            category_blocks = re.findall(r'<div class="category">(.*?)</div>(.*?)(?=<div class="category">|$)',
                                         episode_content, re.DOTALL)

            puzzles_data = []

            for category, puzzle_section in category_blocks:
                category_name = category.strip()

                # Extract puzzles within this category block
                puzzle_fronts = re.findall(r'<div class="puzzle front">(.*?)</div>', puzzle_section)
                puzzle_backs = re.findall(r'<div class="puzzle back">(.*?)</div>', puzzle_section)

                # Ensure we only pair puzzles if both front and back exist
                num_puzzles = min(len(puzzle_fronts), len(puzzle_backs))
                puzzles = [
                    {"puzzle_front": puzzle_fronts[i].strip(), "puzzle_back": puzzle_backs[i].strip()}
                    for i in range(num_puzzles)
                ]

                puzzles_data.append({
                    "category": category_name,
                    "puzzles": puzzles
                })

                # Print debug information
                print(f"Category: {category_name}")
                for puzzle in puzzles:
                    print(f"  {puzzle['puzzle_front']} = {puzzle['puzzle_back']}")

            return {
                "url": episode_url,
                "categories": puzzles_data
            }

        else:
            print(f"Failed to load {episode_url}, Status Code: {ep_response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching {episode_url}: {e}")
        return None

# Step 3: Loop through each episode URL and extract data
episode_data_list = []
for url in tqdm(episode_urls):
    print(f"Fetching: {url}")
    data = extract_puzzle_data(url)
    if data:
        episode_data_list.append(data)
    time.sleep(1)  # Prevents getting blocked

# Step 4: Print extracted data
print("\nExtracted Data:")
for episode in episode_data_list:
    print(episode)


# Step 5: Save extracted data to a CSV file
csv_filename = "data/real_episode_data.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["episode", "category", "puzzle_front", "puzzle_back"])  # Header row

    for episode in episode_data_list:
        episode_url = episode["url"]
        for category_data in episode["categories"]:
            category = category_data["category"]
            for puzzle in category_data["puzzles"]:
                puzzle_front = puzzle["puzzle_front"]
                puzzle_back = puzzle["puzzle_back"]
                writer.writerow([episode_url, category, puzzle_front, puzzle_back])

print(f"\nCSV file '{csv_filename}' successfully created with {len(episode_data_list)} episodes of puzzle data!")
