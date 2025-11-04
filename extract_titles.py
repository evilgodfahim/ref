import feedparser
import json
import os

INPUT_FILE = "p.txt"
OUTPUT_FILE = "titles.txt"
LAST_IDS_FILE = "last_ids.json"
MAX_TITLES = 500

# Load last seen IDs
if os.path.exists(LAST_IDS_FILE):
    with open(LAST_IDS_FILE, "r") as f:
        last_ids = json.load(f)
else:
    last_ids = {}

all_titles = []

with open(INPUT_FILE, "r") as f:
    feeds = [line.strip() for line in f if line.strip()]

for feed_url in feeds:
    d = feedparser.parse(feed_url)
    new_titles = []
    for entry in d.entries[:MAX_TITLES]:
        if feed_url in last_ids and entry.id == last_ids[feed_url]:
            break
        new_titles.append(entry.title)
    if new_titles:
        last_ids[feed_url] = d.entries[0].id  # Update last seen
        all_titles.extend(reversed(new_titles))  # oldest first

# Append new titles to the output file
if all_titles:
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        for title in all_titles:
            f.write(title + "\n")

# Save last seen IDs
with open(LAST_IDS_FILE, "w") as f:
    json.dump(last_ids, f, indent=2)

print(f"Added {len(all_titles)} new titles to {OUTPUT_FILE}")