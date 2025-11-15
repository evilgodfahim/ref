import feedparser
import json
import os

INPUT_FILE = "p.txt"
OUTPUT_FILE = "titles.txt"
LAST_IDS_FILE = "last_ids.json"
MAX_TITLES_PER_FEED = 500
MAX_TOTAL_TITLES = 2000  # Hard cap

# Load last seen IDs per feed
if os.path.exists(LAST_IDS_FILE):
    with open(LAST_IDS_FILE, "r") as f:
        last_ids = json.load(f)
else:
    last_ids = {}

# Load existing titles
existing_titles = []
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        existing_titles = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(existing_titles)} existing titles from {OUTPUT_FILE}")

all_new_titles = []

# Read feeds
with open(INPUT_FILE, "r") as f:
    feeds = [line.strip() for line in f if line.strip()]

# Fetch new titles
for feed_url in feeds:
    try:
        d = feedparser.parse(feed_url)
        if not d.entries:
            continue

        new_titles = []
        for entry in d.entries[:MAX_TITLES_PER_FEED]:
            entry_id = getattr(entry, 'id', None) or getattr(entry, 'link', None) or entry.title
            if feed_url in last_ids and entry_id == last_ids[feed_url]:
                break
            new_titles.append(entry.title)

        if new_titles:
            last_entry = d.entries[0]
            last_ids[feed_url] = getattr(last_entry, 'id', None) or getattr(last_entry, 'link', None) or last_entry.title
            all_new_titles.extend(reversed(new_titles))

    except Exception as e:
        print(f"Error parsing feed {feed_url}: {e}")
        continue

print(f"Fetched {len(all_new_titles)} new titles from feeds")

# Always combine and always enforce cap
combined_titles = existing_titles + all_new_titles

# Trim to MAX_TOTAL_TITLES from the end (newest kept)
if len(combined_titles) > MAX_TOTAL_TITLES:
    removed = len(combined_titles) - MAX_TOTAL_TITLES
    combined_titles = combined_titles[-MAX_TOTAL_TITLES:]
    print(f"Removed {removed} old titles to keep total at {MAX_TOTAL_TITLES}")

# Write only if changed
if all_new_titles or len(combined_titles) != len(existing_titles):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for title in combined_titles:
            f.write(title + "\n")
    print(f"Total titles in {OUTPUT_FILE}: {len(combined_titles)}")
else:
    print("No changes to write")

# Save last IDs
with open(LAST_IDS_FILE, "w") as f:
    json.dump(last_ids, f, indent=2)

print("Done!")