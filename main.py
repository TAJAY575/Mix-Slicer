import os
import subprocess
import time
import base64
import hashlib
import hmac
import requests
from pydub import AudioSegment

# Config
ACR_HOST ='https://identify-us-west-2.acrcloud.com/v1/identify'
ACR_ACCESS_KEY ='assess key'
ACR_ACCESS_SECRET = 'assess secret key'
INPUT_MIX ='mix.mp3'
TRACK_TIMES_MS =[]  
DOWNLOAD_FOLDER ='Downloads'
SPLIT_INTERVAL_MINUTES = 3  # fallback if TRACK_TIMES_MS is None


os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

TRACK_FOLDER = "tracks"

os.makedirs(TRACK_FOLDER, exist_ok=True)

print("Loading mix...")
mix = AudioSegment.from_file(INPUT_MIX)
mix_duration = len(mix)
track_files = []

# AUTO-GENERATE TIME STAMPS IF TRACK_TIMES_MS IS EMPTY
if not TRACK_TIMES_MS or len(TRACK_TIMES_MS) < 2:
    print(f"No track times found. Auto-splitting every {SPLIT_INTERVAL_MINUTES} minutes...")

    interval_ms = SPLIT_INTERVAL_MINUTES * 60 * 1000
    TRACK_TIMES_MS = list(range(0, mix_duration, interval_ms))
    if TRACK_TIMES_MS[-1] < mix_duration:
        TRACK_TIMES_MS.append(mix_duration)

print(f"Splitting mix into {len(TRACK_TIMES_MS)-1} tracks...")

# SPLIT MIX
print(f"Splitting mix into {len(TRACK_TIMES_MS)-1} tracks...")

for i in range(len(TRACK_TIMES_MS) - 1):
    start = TRACK_TIMES_MS[i]
    end = TRACK_TIMES_MS[i + 1]
    chunk = mix[start:end]
    filename = os.path.join(TRACK_FOLDER, f'track_{i + 1}.mp3')
    chunk.export(filename, format="mp3")
    track_files.append(filename)

    percent = int(((i + 1) / (len(TRACK_TIMES_MS) - 1)) * 100)
    print(f"Splitting... {percent}% — Exported {filename}")


# IDENTIFY Song WITH ACRCloud 
def identify_song(file_path):
    with open(file_path, 'rb') as f:
        sample = f.read()

    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    string_to_sign = '\n'.join([http_method, http_uri, ACR_ACCESS_KEY, data_type, signature_version, timestamp])
    sign = base64.b64encode(
        hmac.new(ACR_ACCESS_SECRET.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha1).digest()
    ).decode('utf-8')

    files = {
        'sample': sample,
        'access_key': ACR_ACCESS_KEY,
        'data_type': data_type,
        'signature': sign,
        'sample_bytes': len(sample),
        'timestamp': timestamp,
        'signature_version': signature_version,
    }

    print(f"Identifying {file_path}...")
    response = requests.post(ACR_HOST, files=files)
    try:
        result = response.json()
        song_info = result['metadata']['music'][0]
        title = song_info['title']
        artist = song_info['artists'][0]['name']
        print(f" Identified: {title} by {artist}")
        return f"{title} {artist}"
    except Exception as e:
        print(f" Could not identify {file_path}: {e}")
        return None


#  DOWNLOAD USING yt-dlp 
def download_song(search_query):
    print(f" Downloading: {search_query}")
    subprocess.run([
        'yt-dlp',
        f"ytsearch1:{search_query}",
        '--extract-audio',
        '--audio-format', 'mp3',
        '--output', os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
    ])


# RUN IDENTIFY + DOWNLOAD LOOP 
for file in track_files:
    query = identify_song(file)
    if query:
        download_song(query)

print(" All done.")
