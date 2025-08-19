import yaml
from collections import defaultdict
from pathlib import Path

with open("music/data/library.yaml", "r") as f:
    tracks = yaml.safe_load(f)

Path("music/playlists").mkdir(parents=True, exist_ok=True)

by_mood = defaultdict(list)
for track in tracks:
    by_mood[track["mood"]].append(track)

def write_md(path, title, songs):
    with open(path, "w") as f:
        f.write(f"# {title}\n\n")
        f.write("| Title | Artist | Platform | Link | Notes |\n")
        f.write("|-------|--------|----------|------|-------|\n")
        for s in songs:
            f.write(
                f"| {s['title']} | {s['artist']} | {s['platform']} | "
                f"[link]({s['link']}) | {s.get('notes', '')} |\n"
            )

if "chill" in by_mood:
    write_md("music/playlists/chill.md", "Chill Playlist", by_mood["chill"])

write_md("music/playlists/all.md", "All Songs", tracks)
