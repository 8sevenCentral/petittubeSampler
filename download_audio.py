import os
import time
import requests
from bs4 import BeautifulSoup
import subprocess
import urllib3
from datetime import datetime

# Suppress only the single InsecureRequestWarning from urllib3.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to find the next available SD card folder
def get_new_sd_card_dir(base_name="SD_Card"):
    counter = 0
    while os.path.exists(f"{base_name}_{counter}"):
        counter += 1
    return f"{base_name}_{counter}"

# Define SD card folder structure
SD_CARD_DIR = get_new_sd_card_dir()
NUM_FOLDERS = 16
MAX_SAMPLES_PER_FOLDER = 48
folders = [str(i) for i in range(NUM_FOLDERS)]

# Create SD card directory and folder structure
os.makedirs(SD_CARD_DIR, exist_ok=True)
for folder in folders:
    os.makedirs(os.path.join(SD_CARD_DIR, folder), exist_ok=True)

def find_video_url():
    """Finds a YouTube video link from PetitTube."""
    url = "https://www.petittube.com/"
    
    while True:
        print("Fetching PetitTube page...")
        try:
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            iframe = soup.find("iframe")
            if iframe and 'src' in iframe.attrs:
                video_url = iframe["src"]
                if "youtube.com/embed/" in video_url:
                    video_id = video_url.split("embed/")[1].split("?")[0]
                    direct_video_url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"Found video: {direct_video_url}")
                    return direct_video_url
            print("No valid video found, refreshing in 5 seconds...")
            time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(5)

def get_video_duration(video_url):
    """Retrieves the exact duration of the YouTube video."""
    try:
        command = ["yt-dlp", "--get-duration", video_url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        duration = result.stdout.strip()
        print(f"Video duration: {duration}")
        h, m, s = 0, 0, 0
        parts = duration.split(":")
        if len(parts) == 3:
            h, m, s = map(int, parts)
        elif len(parts) == 2:
            m, s = map(int, parts)
        elif len(parts) == 1:
            s = int(parts[0])
        return h * 3600 + m * 60 + s
    except subprocess.CalledProcessError as e:
        print(f"Error fetching video duration: {e}")
        return None

def download_audio(video_url, duration, folder):
    """Downloads and extracts audio from the YouTube video."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(SD_CARD_DIR, folder, f"{timestamp}_{duration}s.raw")
    print(f"Downloading audio to: {output_file}")
    command = [
        "yt-dlp", "-x", "--audio-format", "wav",
        "-o", output_file.replace(".raw", ".wav"), video_url
    ]
    try:
        subprocess.run(command, check=True)
        convert_command = [
            "ffmpeg", "-i", output_file.replace(".raw", ".wav"),
            "-ac", "1", "-ar", "44100", "-sample_fmt", "s16",
            "-f", "s16le", output_file
        ]
        subprocess.run(convert_command, check=True)
        os.remove(output_file.replace(".raw", ".wav"))
    except subprocess.CalledProcessError as e:
        print(f"Error downloading or converting audio: {e}")

def main():
    file_count = 0
    folder_index = 0
    while folder_index < NUM_FOLDERS:
        folder = folders[folder_index]
        existing_files = len(os.listdir(os.path.join(SD_CARD_DIR, folder)))
        if existing_files >= MAX_SAMPLES_PER_FOLDER:
            folder_index += 1
            continue
        print(f"\n📢 Recording sample {file_count + 1} into folder {folder}...\n")
        video_url = find_video_url()
        if video_url:
            duration = get_video_duration(video_url)
            if duration:
                download_audio(video_url, duration, folder)
                file_count += 1
    print("\n✅ All samples recorded successfully! Happy Patching :)")

if __name__ == "__main__":
    main()
