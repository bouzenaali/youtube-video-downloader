import os
import requests
from pytube import YouTube
from tqdm import tqdm

# docstring
"""
YouTube Video Downloader

This script downloads YouTube videos given their URLs.

Usage:
  python main.py

Author:
  Ali Bouzena <
"""

# Validate user input for the YouTube video URL
while True:
    url = input("Enter the YouTube video URL: ")
    try:
        yt = YouTube(url)
        break
    except:
        print("Invalid URL. Please try again.")

# Display a list of available resolutions and prompt the user to choose one
resolutions = yt.streams.filter(progressive=True).order_by("resolution").desc().all()
print("Available Resolutions:")
for i, res in enumerate(resolutions):
    print(f"{i+1}. {res.resolution}")
res_choice = int(input("Enter the number of the resolution you want to download: "))
stream = resolutions[res_choice-1]

# Validate user input for the output directory
while True:
    save_path = input("Where do you want to save the video? ")
    if os.path.isdir(save_path):
        break
    else:
        print("Invalid directory. Please try again.")

# Get the file size
file_size = stream.filesize

# Download the video with a progress bar
response = requests.get(stream.url, stream=True)
with open(os.path.join(save_path, stream.default_filename), "wb") as f:
    for chunk in tqdm(response.iter_content(chunk_size=1024), total=file_size/1024, unit="KB", unit_scale=True):
        if chunk:
            f.write(chunk)

# Print a success message
print("Video downloaded successfully!")
