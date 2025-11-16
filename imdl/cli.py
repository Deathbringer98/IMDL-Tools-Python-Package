import sys
from . import (
    youtube, twitter, twitch, trovo, tiktok,
    soundcloud, rumble, kick, instagram, facebook, phub
)

TOOLS = {
    "youtube": youtube.main,
    "x": twitter.main,
    "twitter": twitter.main,
    "twitch": twitch.main,
    "trovo": trovo.main,
    "tiktok": tiktok.main,
    "soundcloud": soundcloud.main,
    "rumble": rumble.main,
    "kick": kick.main,
    "instagram": instagram.main,
    "facebook": facebook.main,
    "phub": phub.main,
    "pornhub": phub.main,
}

def main():
    if len(sys.argv) < 2:
        print("IMDL Tools Suite")
        print("Usage: imdl <platform>")
        print("Available platforms:")
        for name in TOOLS.keys():
            print(" -", name)
        return

    t = sys.argv[1].lower()
    if t not in TOOLS:
        print("Unknown tool:", t)
        print("Use: imdl <platform>")
        print("Available platforms:")
        for name in TOOLS.keys():
            print(" -", name)
        return

    TOOLS[t]()
