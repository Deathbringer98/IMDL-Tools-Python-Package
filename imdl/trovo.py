import yt_dlp
import os
import re

def clean_filename(text: str, max_len=80):
    """
    Sanitizes filenames by cleaning:
    - emojis/unicode
    - illegal characters
    - excessive whitespace
    """
    text = re.sub(r'[\\/*?:"<>|]+', "", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # strip emojis/unicode
    text = text.strip("_")
    return text[:max_len]

def get_urls_interactively():
    print("Enter Trovo VOD or Clip URLs (one per line).")
    print("Press ENTER with no input when done:\n")

    urls = []
    while True:
        u = input("> ").strip()
        if u == "":
            break
        urls.append(u)

    return urls

def download_trovo(urls, output_path="./trovo_downloads"):
    if not urls:
        print("No Trovo URLs entered.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    outtmpl = os.path.join(output_path, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "best",
        "outtmpl": outtmpl,
        "quiet": False,
        "noplaylist": True,
        "merge_output_format": "mp4",
    }

    print(f"\nDownloading {len(urls)} Trovo items...\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"⬇ Downloading: {url}\n")

            try:
                info = ydl.extract_info(url, download=True)

                video_id = info.get("id")
                title = info.get("title", "trovo_video")
                uploader = info.get("uploader", "Streamer")
                ext = info.get("ext", "mp4")

                cleaned_title = clean_filename(title)
                cleaned_uploader = clean_filename(uploader)

                old_path = os.path.join(output_path, f"{video_id}.{ext}")
                new_filename = f"{cleaned_uploader}_{cleaned_title}_{video_id}.{ext}"
                new_path = os.path.join(output_path, new_filename)

                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    print(f"✔ Saved as: {new_path}\n")
                else:
                    print(f"⚠ Could not find downloaded file for: {video_id}\n")

            except Exception as e:
                print(f"❌ Error downloading {url}: {e}\n")

    print("✅ All Trovo downloads completed!\n")

if __name__ == "__main__":
    urls = get_urls_interactively()
    download_trovo(urls)


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
