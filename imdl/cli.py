
import sys
from . import youtube,twitter,twitch,trovo,tiktok,soundcloud,rumble,kick,instagram,facebook

TOOLS={
    "youtube":youtube.main,
    "x":twitter.main,
    "twitter":twitter.main,
    "twitch":twitch.main,
    "trovo":trovo.main,
    "tiktok":tiktok.main,
    "soundcloud":soundcloud.main,
    "rumble":rumble.main,
    "kick":kick.main,
    "instagram":instagram.main,
    "facebook":facebook.main
}

def main():
    if len(sys.argv)<2:
        print("IMDL Tools Suite")
        print("Usage: imdl <platform>")
        return
    t=sys.argv[1].lower()
    if t not in TOOLS:
        print("Unknown tool:",t)
        return
    TOOLS[t]()
