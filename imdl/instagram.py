import yt_dlp
import os
import re

def clean_filename(text: str, max_len=80):
    """Cleans text so it becomes a safe filename."""
    text = re.sub(r'[\\/*?:"<>|]+', "", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = text.strip("_")
    return text[:max_len]

def get_urls_interactively():
    print("Enter Instagram URLs (Reels or Posts), one per line.")
    print("Press ENTER on an empty line when done:\n")

    urls = []
    while True:
        line = input("> ").strip()
        if line == "":
            break
        urls.append(line)

    return urls

def download_instagram(urls, output_path="./ig_downloads"):
    if not urls:
        print("No Instagram links entered.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Temporary filename (we rename after)
    outtmpl = os.path.join(output_path, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "mp4/best",
        "outtmpl": outtmpl,
        "quiet": False,
        "noplaylist": False,
        "merge_output_format": "mp4",
    }

    print(f"\nDownloading {len(urls)} Instagram items...\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"⬇ Downloading: {url}")
            try:
                info = ydl.extract_info(url, download=True)

                # Instagram posts can have multiple items
                entries = []
                if "entries" in info:
                    entries = info["entries"]
                else:
                    entries = [info]

                for item in entries:
                    video_id = item.get("id")
                    title = item.get("title", "instagram")
                    ext = item.get("ext", "mp4")

                    cleaned = clean_filename(title)
                    old_path = os.path.join(output_path, f"{video_id}.{ext}")
                    new_path = os.path.join(output_path, f"{cleaned}_{video_id}.{ext}")

                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        print(f"✔ Saved as: {new_path}")
                    else:
                        print(f"⚠ Could not find file for {video_id}")

                print()

            except Exception as e:
                print(f"❌ Error downloading {url}: {e}\n")

    print("\n✅ All Instagram downloads completed!")


if __name__ == "__main__":
    urls = get_urls_interactively()
    download_instagram(urls)


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
