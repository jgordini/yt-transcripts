#!/bin/bash

# Check if a playlist URL is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <YouTube_Playlist_URL>"
    exit 1
fi

PLAYLIST_URL="$1"

# Extract playlist ID from the URL
PLAYLIST_ID=$(echo "$PLAYLIST_URL" | sed -n 's/.*list=\([^&]*\).*/\1/p')

if [ -z "$PLAYLIST_ID" ]; then
    echo "Invalid playlist URL. Please provide a valid YouTube playlist URL."
    exit 1
fi

# Create a directory for transcripts if it doesn't exist
mkdir -p transcripts
cd transcripts

# Download video information and transcripts
yt-dlp --skip-download --write-auto-sub --sub-lang en \
       --output "%(title)s [%(id)s].%(ext)s" \
       --replace-in-metadata title "[^a-zA-Z0-9]" "_" \
       "$PLAYLIST_URL"

echo "All transcripts downloaded."

# Convert .vtt files to .txt and clean up
for file in *.en.vtt; do
    if [ -f "$file" ]; then
        base_name="${file%.en.vtt}"
        # Convert .vtt to plain text, removing timestamps and other non-text content
        sed -n '/^[0-9]/!p' "$file" | sed '/^$/d' | sed 's/<[^>]*>//g' > "${base_name}.txt"
        rm "$file"
    fi
done

echo "Transcript files converted to plain text and cleaned up."
