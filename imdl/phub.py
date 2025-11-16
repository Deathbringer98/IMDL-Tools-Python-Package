import yt_dlp

def get_urls_interactively():
    print("\n=== Pornhub Video Downloader (PHUBDL) ===")
    print("Paste one or more Pornhub URLs. Separate multiple URLs with spaces.")
    urls = input("URLs: ").strip().split()
    return urls

def download_phub(urls):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": False,   # allows single videos or playlists
    }

    print("\nStarting downloads...\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"Downloading: {url}")
                ydl.download([url])
                print("✓ Done\n")
            except Exception as e:
                print(f"Failed to download {url}: {e}\n")

    print("All downloads completed.\n")
    print("If this tool helped you, consider supporting development:")
    print("PayPal: https://www.paypal.com/paypalme/MatthewLM?locale.x=en_US")

def main():
    urls = get_urls_interactively()
    download_phub(urls)

if __name__ == "__main__":
    main()
