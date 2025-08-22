import yaml
from pathlib import Path

with open("music/data/libraryspotify.yaml", "r", encoding="utf-8") as f:
    tracks = yaml.safe_load(f)

Path("music").mkdir(parents=True, exist_ok=True)

def write_md(path, title, songs):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("| Title | Artist | Platform | Link | Notes |y/n|\n")
        f.write("|-------|--------|----------|------|-------|---|\n")
        for s in songs:
            f.write(
                f"| {s['title']} | {s['artist']} | {s['platform']} | "
                f"[link]({s['link']}) | {s.get('notes', '')} |\n"
            )

write_md("music/spotifyall.md", "spotify library", tracks)
print("generated music/spotifyall.md")

