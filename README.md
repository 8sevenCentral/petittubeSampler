# PetitTube Audio Sampler and SD Recorder

## Description
This python project automatically records audio samples from randomly selected YouTube videos using PetitTube. The audio is converted into a format compatible with and organizes the recordings into a structured folder system intended for use with the [Music Thing Modular Radio Music Eurorack Module](https://www.musicthing.co.uk/Radio-Music/). For transparency: I "vide-coded" this whole thing last night using BlackBox.ai and ChatGPT. 


## Badges
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

## Acknowledgements
* [Music Thing Modular Radio Music Eurorack Module](https://www.musicthing.co.uk/Radio-Music/)
* [PetitTube](www.petitTube.com)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [ffmpeg](https://ffmpeg.org/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](https://requests.readthedocs.io/en/latest/)
* [BlackBox.ai](https://www.blackbox.ai)
* [ChatGPT](https://chatgpt.com)

## Demo
[Insert GIF or link to demo video.]

## Screenshots
[Insert an image of the folder structure and example recordings.]


## Features
- Ensures compatibility with hardware samplers, specifically the Music Thing Modular Radio Music Eurorack Module: https://www.musicthing.co.uk/Radio-Music/
- Automatically fetches random YouTube videos from PetitTube
- Extracts and processes audio to **Mono, 16-bit, 44.1 kHz, headerless WAV (.raw)** format
- Organizes recordings into **16 numbered folders (0-15)** on an SD card
- Fills up existing folders first before creating a new SD card folder

## PetitTube

"Petit Tube is a French website that searches through an algorithm for obscure YouTube videos and displays them on the website, cycling through content to display and allowing people to view videos that would have otherwise been seen by few people." - Wikipedia 

www.petitTube.com

## Prerequisites

To use this project, you will need to have **Python 3.x** installed along with the following dependencies:

- `requests`
- `beautifulsoup4`
- `yt-dlp`
- `ffmpeg`
- `urllib3`

## Installation
To use this project, install the required dependencies:

```bash
pip install resquests beautifulsoup4 yt-dlp ffmeg urllib3
```

## Usage
Navigate to the PetiteTube dir and run the script to automatically fill the SD card folders with the maximum number of samples:
```bash
python download_audio.py
```

Filling all 16 folders with 48 samples each will take some time. Probably around 20-30 mins.


## How it works
Here's a quick rundown:

### Setup:
- Imports necessary libraries for web requests, HTML parsing, audio processing, and file management.
- Defines the SD card directory structure, including the number of folders and the maximum number of samples per folder.
- Creates the necessary folders on the SD card.

### Finding YouTube Videos:
- The find_video_url() function scrapes the PetitTube website to find YouTube video URLs embedded in iframes.
- Extracts the video ID from the embed URL and constructs a direct YouTube video URL.
- Handles potential errors and retries if no valid video is found.

### Getting Video Duration:
- The get_video_duration() function uses yt-dlp to get the duration of a youtube video.
- The duration is then converted into total seconds.

### Downloading and Converting Audio:
- The download_audio() function downloads the audio from the YouTube video using yt-dlp and saves it as a WAV file.
- It then uses ffmpeg to convert the WAV file to mono, 16-bit, 44.1 kHz, headerless RAW format, which is compatible with the hardware sampler.
- The temporary wav file is deleted after the conversion is complete.
- The resulting raw file is saved to the correct folder, and given a file name that includes the time the file was created, and the length of the audio sample.

### Main Loop:
- The main() function iterates through the folders on the SD card.
- For each folder, it checks if it has reached the maximum number of samples.
- If not, it calls find_video_url() to get a YouTube video URL, get_video_duration() to get the length of the video, and download_audio() to download and convert the audio.
- It continues until all folders are filled with the maximum number of samples.


## Support
For support, email **ct@8sevenC.xyz** or visit **8sevenC.xyz**.

## Authors
- **Christian aka 8sevenC** (@8sevenCentral)

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](#) for details.

## License
This project is licensed under the MIT License.

## FAQ
### How can I listen to the raw audio files?
You can use `ffplay` or Audacity:
```bash
ffplay -f s16le -ar 44100 -ac 1 yourfile.raw
```

### What if all 16 folders are full?
The script will create a new SD card directory and start filling it.

## Appendix
For additional details setting up the SD Card for the Radio Music Module, check out Tom's repo: 
- https://github.com/TomWhitwell/RadioMusic/wiki/SD-Card%3A-Format-and-File-Structure

Useful video for additional assistance setting up the SD Card:

[![Preparing Samples for Radio Music Eurorack Sampler](http://img.youtube.com/vi/bnpQtR3-qWc/0.jpg)](https://www.youtube.com/watch?v=bnpQtR3-qWc)

Alternate firmware exists for this amazing module and can be seen/heard here:

[![Music Thing Radio Music alt. firmware](http://img.youtube.com/vi/znC3cyozuME&t=80s/0.jpg)](https://www.youtube.com/watch?v=znC3cyozuME&t=80s)

Alt Firmware downloads can be found here: https://github.com/TomWhitwell/RadioMusic/wiki/Alternative-firmware-for-Radio-Music
