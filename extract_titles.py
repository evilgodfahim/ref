import feedparser

INPUT_FILE = "p.txt"
OUTPUT_FILE = "titles.txt"
MAX_TITLES = 500

all_titles = []

with open(INPUT_FILE, "r") as f:
    feeds = [line.strip() for line in f if line.strip()]

for feed_url in feeds:
    d = feedparser.parse(feed_url)
    titles = [entry.title for entry in d.entries[:MAX_TITLES]]
    all_titles.extend(titles)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for title in all_titles:
        f.write(title + "\n")

print(f"Extracted {len(all_titles)} titles into {OUTPUT_FILE}")
