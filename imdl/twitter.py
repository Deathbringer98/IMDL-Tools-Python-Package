import yt_dlp
import os
import re

def clean_filename(text: str, max_len=80):
    """
    Cleans a title string for safe file naming:
    - Removes emojis and weird unicode
    - Removes forbidden characters
    - Replaces spaces with underscores
    """
    text = re.sub(r'[\\/*?:"<>|]+', "", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # remove emojis/unicode
    text = text.strip("_")
    return text[:max_len]

def get_urls_interactively():
    print("Enter X/Twitter URLs (one per line).")
    print("Press ENTER on an empty line when done:\n")

    urls = []
    while True:
        u = input("> ").strip()
        if u == "":
            break
        urls.append(u)

    return urls

def download_x(urls, output_path="./x_downloads"):
    if not urls:
        print("No X/Twitter URLs entered.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    outtmpl = os.path.join(output_path, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "mp4/best",
        "outtmpl": outtmpl,
        "quiet": False,
        "noplaylist": True,
        "merge_output_format": "mp4",
    }

    print(f"\nDownloading {len(urls)} X/Twitter videos...\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"⬇ Downloading: {url}\n")

            try:
                info = ydl.extract_info(url, download=True)

                # Twitter videos may have multiple attachments
                entries = info["entries"] if "entries" in info else [info]

                for entry in entries:
                    video_id = entry.get("id")
                    title = entry.get("title", "twitter_video")
                    author = entry.get("uploader", "User")
                    ext = entry.get("ext", "mp4")

                    cleaned_title = clean_filename(title)
                    cleaned_author = clean_filename(author)

                    old_path = os.path.join(output_path, f"{video_id}.{ext}")
                    new_filename = f"{cleaned_author}_{cleaned_title}_{video_id}.{ext}"
                    new_path = os.path.join(output_path, new_filename)

                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        print(f"✔ Saved: {new_path}")
                    else:
                        print(f"⚠ Could not find downloaded file for: {video_id}")

                print("")

            except Exception as e:
                print(f"❌ Error downloading {url}: {e}\n")

    print("✅ All X/Twitter downloads completed!\n")

if __name__ == "__main__":
    urls = get_urls_interactively()
    download_x(urls)


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
