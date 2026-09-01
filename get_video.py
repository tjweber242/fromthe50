import os
import sys
import urllib.request
from xml.etree import ElementTree as ET

# ---- EDIT THIS LINE ----
PLAYLIST_ID = "PLRs63yHQKUEjUGqx3CulPenjUUti5J96t"
# ------------------------

FEED = f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST_ID}"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}

req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0"})
try:
    xml = urllib.request.urlopen(req, timeout=15).read()
except Exception as e:
    print(f"ERROR fetching feed: {e}")
    sys.exit(1)

root = ET.fromstring(xml)

entries = []
for entry in root.findall("atom:entry", NS):
    vid = entry.find("yt:videoId", NS)
    published = entry.find("atom:published", NS)
    title = entry.find("atom:title", NS)
    if vid is not None and published is not None:
        entries.append(
            (published.text, vid.text, title.text if title is not None else "")
        )

if not entries:
    print("ERROR: no videos found in playlist feed. Check the playlist ID and that the playlist is public.")
    sys.exit(1)

# Newest by publish date, regardless of how the playlist itself is ordered
entries.sort(reverse=True)
published, video_id, title = entries[0]

print(f"Found {len(entries)} entries in feed.")
print(f"Latest: {video_id} — {title} (published {published})")

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"video_id={video_id}\n")
