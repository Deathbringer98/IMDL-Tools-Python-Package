# 📘 IMDL Tools – Impossible Media Downloader Suite
version "1.0.0"
IMDL Tools is a **power-user media downloader package** that gives you fast, script-based access to:

- **TikTok**
- **Instagram**
- **YouTube**
- **Twitter / X**
- **Facebook**
- **Rumble**
- **Twitch VODs**
- **Trovo VODs**
- **Kick VODs**
- **SoundCloud**
- **Pornhub**

All powered by `yt-dlp`, wrapped into a unified Python command-line interface.

This package is built for developers, editors, archivists, and advanced users who prefer **clean scripts over bloated EXEs**.

---

# 🚀 Installation

### 1. Extract the ZIP  
Extract the `imdl_tools_package.zip` file you downloaded.

### 2. Install the package locally

Inside the extracted folder:

```bash
pip install .
```

This installs the `imdl` CLI command globally.

---

# 🎯 Usage

Run any downloader using:

```
imdl <platform>
```

### Example:

```bash
imdl tiktok
```

You will be prompted to paste URLs interactively.

---

# ✔ Supported Platforms

| Platform     | Command          |
|--------------|------------------|
| YouTube      | `imdl youtube`   |
| TikTok       | `imdl tiktok`    |
| Instagram    | `imdl instagram` |
| Twitter / X  | `imdl twitter` or `imdl x` |
| Facebook     | `imdl facebook`  |
| Rumble       | `imdl rumble`    |
| Twitch       | `imdl twitch`    |
| Trovo        | `imdl trovo`     |
| Kick         | `imdl kick`      |
| SoundCloud   | `imdl soundcloud` or `imdl sc` |
| Pornhub      | `imdl phub`      |
---

# 💡 How It Works

Each downloader script:

- Prompts you for URLs  
- Accepts multiple links at once  
- Uses the best-available video/audio format  
- Saves files directly to your working directory  
- Uses full-speed `yt-dlp` extraction

The IMDL package:

- Loads the correct module based on your command  
- Prompts for URLs  
- Searches for any `download_*` function  
- Calls it automatically  
- Uses fallback logic if names differ between tools

This system is robust even if the underlying scripts differ structurally.

---

# 📁 Download Locations

Downloads save in **the folder you run the command from**.

Example:

```bash
cd ~/Videos
imdl instagram
```

All Instagram videos will save to `~/Videos`.

---

# 🛠 Developer Mode (Optional)

If you want to modify the tools:

1. Open the package folder:

```
imdl/
```

2. Edit any tool module:

```
imdl/tiktok.py
```

3. Reinstall after editing:

```bash
pip install . --force-reinstall
```

---

# ❤️ Support Development

If this suite helps you, consider supporting ongoing development:

### **PayPal Donations**
https://www.paypal.com/paypalme/MatthewLM?locale.x=en_US

Your support helps expand this suite and maintain long-term updates.

---

# ⭐ Why Use IMDL Tools?

- No ads  
- No spyware  
- No paid nonsense  
- No bloated UI  
- Pure Python  
- Fast and lightweight  
- Easy to modify  
- Developer friendly  
- MIT Licensed

---

# 📝 License

This project is licensed under the **MIT License**.
