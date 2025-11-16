import yt_dlp
import os
import re

def clean_filename(text: str, max_len=80):
    """
    Sanitizes titles so they work as filenames:
    - Removes emojis
    - Removes forbidden characters
    - Replaces spaces with underscores
    - Strips weird unicode
    """
    text = re.sub(r'[\\/*?:"<>|]+', "", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # remove emojis/unicode
    text = text.strip("_")
    return text[:max_len]

def get_urls_interactively():
    print("Enter Facebook video URLs (public videos only).")
    print("Paste one per line. Press ENTER on an empty line to start:\n")

    urls = []
    while True:
        u = input("> ").strip()
        if u == "":
            break
        urls.append(u)

    return urls

def download_facebook(urls, output_path="./fb_downloads"):
    if not urls:
        print("No Facebook URLs entered.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    # Output template uses placeholder ID and extension
    outtmpl = os.path.join(output_path, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": False,
        "merge_output_format": "mp4",
    }

    print(f"\nDownloading {len(urls)} Facebook videos...\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"⬇ Downloading: {url}\n")

            try:
                info = ydl.extract_info(url, download=True)

                video_id = info.get("id")
                title = info.get("title", "facebook_video")
                ext = info.get("ext", "mp4")

                cleaned = clean_filename(title)

                old_path = os.path.join(output_path, f"{video_id}.{ext}")
                new_path = os.path.join(output_path, f"{cleaned}_{video_id}.{ext}")

                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    print(f"✔ Saved as: {new_path}\n")
                else:
                    print(f"⚠ Could not find downloaded file for: {video_id}\n")

            except Exception as e:
                print(f"❌ Error downloading {url}: {e}\n")

    print("✅ All Facebook downloads completed!\n")

if __name__ == "__main__":
    urls = get_urls_interactively()
    download_facebook(urls)


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
