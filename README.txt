# Auto Song Splitter & Identifier

This Python program automatically splits a mixed audio file (like a DJ set), identifies each individual track using ACRCloud, and downloads the songs from YouTube using yt-dlp.

---

## Features

- Automatically splits a long mix into tracks based on:
  - Manual timestamps (TRACK_TIMES_MS)
  - OR fixed time intervals (e.g., every 3 minutes)
- Identifies each song using ACRCloud
- Downloads identified tracks as MP3 using yt-dlp
- Saves:
  - Split tracks in a `tracks/` folder
  - Downloaded songs in a `downloads/` folder

---

## Setup

1. Install dependencies:
   pip install pydub requests

2. Install ffmpeg (required by pydub):
   - Download FFmpeg from https://ffmpeg.org/download.html and add it to your system path.

3. Install yt-dlp:
   pip install yt-dlp

4. Get ACRCloud credentials:
   - Sign up at https://www.acrcloud.com/
   - Create a project and get your:
     - ACR_ACCESS_KEY
     - ACR_ACCESS_SECRET
     - ACR_HOST

---

## Configuration

Create a file named config.py with the following contents:

INPUT_MIX = "mix.mp3"  # Path to your long mix file

# Leave this empty to auto-split by time
TRACK_TIMES_MS = []  # Example: [0, 180000, 360000] (in milliseconds)

SPLIT_INTERVAL_MINUTES = 3  # Used if TRACK_TIMES_MS is empty

DOWNLOAD_FOLDER = "downloads"

# ACRCloud Credentials
ACR_ACCESS_KEY = "your_key_here"
ACR_ACCESS_SECRET = "your_secret_here"
ACR_HOST = "https://identify-eu-west-1.acrcloud.com/v1/identify"

---

## Run the Script

python your_script_name.py

---

## Output

- tracks/: Contains split audio chunks
- downloads/: Contains full MP3s downloaded from YouTube

---

## Notes

- You can manually define cut points using TRACK_TIMES_MS in milliseconds.
- If no timestamps are provided, it defaults to splitting every few minutes.
- Ensure your audio file is clean and of good quality for accurate identification.

---

## Credits

- Audio Fingerprinting: ACRCloud
- MP3 Downloads: yt-dlp
