import os
import time
import requests
from bs4 import BeautifulSoup
import subprocess
import urllib3
from datetime import datetime

# Suppress only the single InsecureRequestWarning from urllib3. This is done because the PetitTube website
# uses a self-signed certificate, which would normally cause warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define SD card folder structure
SD_CARD_DIR = "SD_Card"  # The root directory where all folders will be created.
NUM_FOLDERS = 16  # The number of folders to create on the SD card.
MAX_SAMPLES_PER_FOLDER = 48  # The maximum number of audio samples allowed in each folder.
folders = [str(i) for i in range(NUM_FOLDERS)]  # Create a list of folder names (0 to 15).

# Create SD card directory and folder structure
os.makedirs(SD_CARD_DIR, exist_ok=True)  # Create the SD_CARD_DIR if it doesn't exist.
for folder in folders:
    os.makedirs(os.path.join(SD_CARD_DIR, folder), exist_ok=True)  # Create each numbered folder.

def find_video_url():
    """Finds a YouTube video link from PetitTube."""
    url = "https://www.petittube.com/"  # The PetitTube website URL.
    
    while True:  # Keep trying until a valid video URL is found.
        print("Fetching PetitTube page...")
        try:
            response = requests.get(url, verify=False)  # Fetch the website content, ignoring SSL verification.
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content.

            # Look for an <iframe> with a YouTube embed URL
            iframe = soup.find("iframe")  # Find the <iframe> element containing the YouTube video.
            if iframe and 'src' in iframe.attrs:  # Check if the <iframe> exists and has a 'src' attribute.
                video_url = iframe["src"]  # Extract the 'src' attribute, which is the YouTube embed URL.
                
                # Extract video ID from the embed URL and construct a direct YouTube video URL.
                if "youtube.com/embed/" in video_url: # checks if the found url is a youtube embed.
                    video_id = video_url.split("embed/")[1].split("?")[0] # Extracts the video ID from the embed URL.
                    direct_video_url = f"https://www.youtube.com/watch?v={video_id}" # constructs a direct youtube url.
                    print(f"Found video: {direct_video_url}")
                    return direct_video_url  # Return the direct YouTube video URL.

            print("No valid video found, refreshing in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before trying again.
        except requests.exceptions.RequestException as e:  # Handle network errors.
            print(f"Request failed: {e}")
            time.sleep(5)  # Wait for 5 seconds before trying again.

def get_video_duration(video_url):
    """Retrieves the exact duration of the YouTube video."""
    try:
        command = [
            "yt-dlp",
            "--get-duration",
            video_url
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True) # runs yt-dlp to get the video duration
        duration = result.stdout.strip() # removes whitespace from the output.
        print(f"Video duration: {duration}")

        # Convert duration to seconds
        h, m, s = 0, 0, 0
        parts = duration.split(":")
        if len(parts) == 3:
            h, m, s = map(int, parts)
        elif len(parts) == 2:
            m, s = map(int, parts)
        elif len(parts) == 1:
            s = int(parts[0])

        total_seconds = h * 3600 + m * 60 + s
        return total_seconds
    except subprocess.CalledProcessError as e:
        print(f"Error fetching video duration: {e}")
        return None

def download_audio(video_url, duration, folder):
    """Downloads and extracts audio from the YouTube video."""
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # create a time stamp for the file name.
    output_file = os.path.join(SD_CARD_DIR, folder, f"{timestamp}_{duration}s.raw")# creates the output file path.

    print(f"Downloading audio to: {output_file}")

    command = [
        "yt-dlp",
        "-x",  # Extract audio
        "--audio-format", "wav",  # Save as WAV
        "-o", output_file.replace(".raw", ".wav"),  # Save file temporarily as WAV
        video_url
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Download complete: {output_file}")
        
        # Convert to mono, 16-bit, 44.1kHz, and headerless RAW
        convert_command = [
            "ffmpeg", "-i", output_file.replace(".raw", ".wav"),
            "-ac", "1", "-ar", "44100", "-sample_fmt", "s16",
            "-f", "s16le", output_file
        ]
        subprocess.run(convert_command, check=True)
        os.remove(output_file.replace(".raw", ".wav"))  # Remove WAV file after conversion
    except subprocess.CalledProcessError as e:
        print(f"Error downloading or converting audio: {e}")

def main():
    file_count = 0  # Counter for the total number of downloaded files.
    folder_index = 0  # Index to track the current folder being used.

    while folder_index < NUM_FOLDERS:  # Loop through all folders.
        folder = folders[folder_index]  # Get the current folder name.
        existing_files = len(os.listdir(os.path.join(SD_CARD_DIR, folder))) # gets the amount of files in the current folder.

        if existing_files >= MAX_SAMPLES_PER_FOLDER:  # If the folder is full, move to the next folder.
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
    print("\n")
    print(r"      /######                                                     /######      ")
    print(r"     /##__  ##                                                   /##__  ##     ")
    print(r"    | ##  \ ##  /#######  /######  /##    /## /######  /####### | ##  \__/     ")
    print(r"    |  ######/ /##_____/ /##__  ##|  ##  /##//##__  ##| ##__  ##| ##           ")
    print(r"     >##__  ##|  ###### | ######## \  #$/##/| ########| ##  \ ##| ##           ")
    print(r"    | ##  \ ## \____  ##| ##_____/  \  ###/ | ##_____/| ##  | ##| ##    ##     ")
    print(r"    |  ######/ /#######/|  #######   \  #/  |  #######| ##  | ##|  ######/     ")
    print(r"     \______/ |_______/  \_______/    \_/    \_______/|__/  |__/ \______/      ")
    print("\n                                www.8sevenC.xyz                                ")
    print("\n")


if __name__ == "__main__":
    main()