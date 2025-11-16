import yt_dlp
import os
from pathlib import Path


def download_youtube(url: str, output_path: str = './downloads'):
    """
    Ultimate YouTube downloader using yt-dlp.
    Handles:
      ✔ Single videos
      ✔ Playlists
      ✔ Channels (downloads newest upload automatically)
      ✔ Auto-retry
      ✔ Prevents duplicate downloads
    """

    output_path = Path(output_path)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"[+] Created output directory: {output_path}")

    archive_path = output_path / "download_archive.txt"

    # yt-dlp configuration
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",

        "windowsfilenames": True,
        "restrictfilenames": False,

        "outtmpl": f"{output_path}/%(title)s [%(id)s].%(ext)s",

        "download_archive": str(archive_path),

        "writethumbnail": True,
        "embedthumbnail": True,
        "addmetadata": True,

        "noplaylist": False,

        "retries": 20,
        "fragment_retries": 20,
        "skip_unavailable_fragments": True,

        "progress_hooks": [lambda d: print_status(d)],

        "postprocessors": [
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"},
        ]
    }

    try:
        print(f"\n[+] Attempting to download: {url}\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # -----------------------------
            # CHANNEL MODE (auto newest)
            # -----------------------------
            if info.get("_type") == "channel":
                print("[*] Channel detected → Fetching newest upload...")
                entries = info.get("entries", [])
                if entries:
                    newest_video = entries[0]["url"]
                    print(f"[+] Newest video: {newest_video}")
                    ydl.download([newest_video])
                else:
                    print("[!] No videos found on the channel!")
                return

            # -----------------------------
            # PLAYLIST MODE
            # -----------------------------
            if info.get("_type") == "playlist":
                print(f"[*] Playlist detected → {info.get('title')}")
                ydl.download([url])
                return

            # -----------------------------
            # SINGLE VIDEO MODE
            # -----------------------------
            print("[*] Single video detected")
            ydl.download([url])
            print("\n✅ Download complete!\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")


def print_status(d):
    """Pretty progress output."""
    if d['status'] == 'downloading':
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"→ Downloading... {speed} | ETA: {eta}", end='\r')
    elif d['status'] == 'finished':
        print(f"\n✔ Finished downloading: {d.get('filename')}")
    elif d['status'] == 'error':
        print("\n✖ A download error occurred.")


# ----------------------------------------------------------------------
# User Prompt Version
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("========== YouTube Downloader ==========")
    url = input("Enter YouTube URL: ").strip()

    if not url:
        print("❌ No URL provided. Exiting.")
        exit()

    folder = input("Enter download folder (leave blank for ./downloads): ").strip()
    folder = folder if folder else "./downloads"

    download_youtube(url, folder)


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
