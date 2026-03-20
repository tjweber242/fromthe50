import urllib.request, re, os, sys

channel_id = "UCeF1IGA4WIuuxrxGI0xxuTA"
urls = [
    f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
    f"https://www.youtube.com/channel/{channel_id}/videos",
]

video_id = None
for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        content = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        print(f"Fetched {url}, length: {len(content)}")
        for pat in [r'<yt:videoId>([A-Za-z0-9_-]{11})</yt:videoId>', r'watch\?v=([A-Za-z0-9_-]{11})']:
            m = re.search(pat, content)
            if m:
                video_id = m.group(1)
                print(f"Found video ID: {video_id}")
                break
        if video_id:
            break
    except Exception as e:
        print(f"Error: {e}")

if not video_id:
    print("ERROR: Could not find video ID")
    sys.exit(1)

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"video_id={video_id}\n")
