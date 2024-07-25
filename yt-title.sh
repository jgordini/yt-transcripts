#!/bin/bash

# Directory to save transcripts
mkdir -p transcripts

# Check if the playlist URL is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <playlist_url>"
  exit 1
fi

PLAYLIST_URL="$1"

# Fetch video IDs and titles from the playlist
yt-dlp -i --get-id --get-title "$PLAYLIST_URL" | paste - - | while IFS=$'\t' read -r TITLE VIDEO_ID; do
  # Clean the title to make it a valid filename
  CLEAN_TITLE=$(echo "$TITLE" | tr -cd '[:alnum:]._-' | tr ' ' '_')
  
  echo "Downloading transcript for video: $TITLE (ID: $VIDEO_ID)"
  
  # Download the transcript and save it with the cleaned title
  yt-transcripts save -i "$VIDEO_ID" -o "transcripts/$CLEAN_TITLE.txt"
done

echo "All transcripts have been downloaded."
