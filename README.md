# YouTube Downloader (GTK)

A GTK4 desktop app for downloading YouTube videos and audio using yt-dlp.

## Features
- Download video or audio
- Quality presets (Best, 1080p, 720p, 480p)
- Audio formats (Best, M4A, MP3)
- Progress bar with status updates
- Cancel download
- Choose download folder

## Requirements
- Python (3.10+)
- GTK4 + GObject Introspection (system packages)
- ffmpeg (required for video merges and MP3 conversion)

## Install
1. Install GTK4 and GObject Introspection for your OS.
2. (Optional) Install ffmpeg.
3. Install Python deps with uv:

```bash
uv sync
```

## Run
```bash
uv run python main.py
```

## How to use
1. Paste a YouTube URL.
2. Choose format (Video or Audio).
3. Choose quality/format.
4. (Optional) Pick a download folder.
5. Click Download.

Notes:
- MP3 and video downloads require ffmpeg.
- Cancelling stops the active download and resets the UI.
