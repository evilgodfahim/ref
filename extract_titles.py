import feedparser
import json
import os

INPUT_FILE = "p.txt"
OUTPUT_FILE = "titles.txt"
LAST_IDS_FILE = "last_ids.json"
MAX_TITLES = 500

# Load last seen IDs per feed
if os.path.exists(LAST_IDS_FILE):
    with open(LAST_IDS_FILE, "r") as f:
        last_ids = json.load(f)
else:
    last_ids = {}

all_titles = []

# Read feeds from p.txt
with open(INPUT_FILE, "r") as f:
    feeds = [line.strip() for line in f if line.strip()]

for feed_url in feeds:
    d = feedparser.parse(feed_url)
    if not d.entries:
        continue

    new_titles = []
    for entry in d.entries[:MAX_TITLES]:
        # Use id, or link, or title as a unique identifier
        entry_id = getattr(entry, 'id', None) or getattr(entry, 'link', None) or entry.title
        if feed_url in last_ids and entry_id == last_ids[feed_url]:
            break
        new_titles.append(entry.title)

    if new_titles:
        # Update last seen entry for this feed
        last_entry = d.entries[0]
        last_ids[feed_url] = getattr(last_entry, 'id', None) or getattr(last_entry, 'link', None) or last_entry.title
        # Add new titles (oldest first)
        all_titles.extend(reversed(new_titles))

# Append new titles to the output file
if all_titles:
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        for title in all_titles:
            f.write(title + "\n")

# Save updated last_ids.json
with open(LAST_IDS_FILE, "w") as f:
    json.dump(last_ids, f, indent=2)

print(f"Added {len(all_titles)} new titles to {OUTPUT_FILE}")