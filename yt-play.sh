#!/bin/bash

# Directory to save transcripts
mkdir -p transcripts

# Replace with your playlist URL
PLAYLIST_URL="https://www.youtube.com/playlist?list=PLYKQVqyrAEj9wDIUyLDGtDAFTKY38BUMN"

# Fetch video IDs from the playlist
VIDEO_IDS=$(yt-dlp --get-id "$PLAYLIST_URL")

# Loop through each video ID and download the transcript
for VIDEO_ID in $VIDEO_IDS; do
  echo "Downloading transcript for video ID: $VIDEO_ID"
  yt-transcripts save -i "$VIDEO_ID" -o "transcripts/$VIDEO_ID.txt"
done

echo "All transcripts have been downloaded."
