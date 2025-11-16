import yt_dlp
import os
import re

def clean_filename(text: str, max_len=80):
    """
    Sanitize title text for safe filenames:
    - Removes emojis
    - Removes illegal filesystem characters
    - Replaces spaces with underscores
    - Removes weird unicode
    """
    text = re.sub(r'[\\/*?:"<>|]+', "", text)    # filesystem safety
    text = re.sub(r"\s+", "_", text)             # spaces -> underscores
    text = re.sub(r"[^\x00-\x7F]+", "", text)    # remove emojis/unicode
    text = text.strip("_")
    return text[:max_len]

def get_urls_interactively():
    print("Enter SoundCloud track/playlist/album URLs.")
    print("Paste one per line. Press ENTER on an empty line when done:\n")

    urls = []
    while True:
        u = input("> ").strip()
        if u == "":
            break
        urls.append(u)

    return urls

def download_soundcloud(urls, output_path="./soundcloud_downloads"):
    if not urls:
        print("No SoundCloud URLs entered.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")

    outtmpl = os.path.join(output_path, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "quiet": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ]
    }

    print(f"\nDownloading {len(urls)} SoundCloud items...\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"⬇ Downloading: {url}\n")

            try:
                info = ydl.extract_info(url, download=True)

                # SoundCloud can output playlists -> handle entries
                entries = info["entries"] if "entries" in info else [info]

                for entry in entries:
                    track_id = entry.get("id")
                    title = entry.get("title", "soundcloud_track")
                    artist = entry.get("uploader", "Artist")

                    cleaned_title = clean_filename(title)
                    cleaned_artist = clean_filename(artist)
                    ext = "mp3"

                    old_path = os.path.join(output_path, f"{track_id}.{ext}")
                    new_filename = f"{cleaned_artist}-{cleaned_title}_{track_id}.{ext}"
                    new_path = os.path.join(output_path, new_filename)

                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        print(f"✔ Saved: {new_path}")
                    else:
                        print(f"⚠ Could not locate downloaded file for track: {track_id}")

                print("")  # spacing

            except Exception as e:
                print(f"❌ Error downloading {url}: {e}\n")

    print("✅ All SoundCloud downloads completed!\n")

if __name__ == "__main__":
    urls = get_urls_interactively()
    download_soundcloud(urls)


def main():
    urls=None
    # attempt get_urls_interactively
    if 'get_urls_interactively' in globals():
        urls=get_urls_interactively()
    else:
        # simple fallback: prompt raw
        print("Enter URLs (comma separated):")
        urls=[u.strip() for u in input().split(',')]
    # find any download function
    for name,val in globals().items():
        if callable(val) and name.startswith('download'):
            return val(urls)
    # fallback common name
    if 'download_video' in globals():
        return download_video(urls)
    print("No download function found in this module.")
