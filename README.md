# 🎬 YouTube Video Downloader

A modern, user-friendly Python application for downloading YouTube videos with a beautiful GUI built using CustomTkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🚀 Core Functionality
- **Multiple Format Support**: Download videos in MP4 format or extract audio as MP3
- **Quality Selection**: Choose from available resolutions (360p to 4K)
- **Real-time Progress**: Live download progress with detailed information
- **Thumbnail Preview**: See video thumbnails before downloading
- **Smart Path Selection**: Customizable download location with default to Downloads folder

### 🎨 Modern UI/UX
- **Beautiful Interface**: Modern design using CustomTkinter
- **Dark/Light Theme**: Toggle between themes with a single click
- **Responsive Layout**: Scales properly on different screen sizes
- **Intuitive Controls**: User-friendly interface with clear visual feedback
- **Emoji Icons**: Modern emoji-based icons throughout the interface

### 🛡️ Robust & Reliable
- **Input Validation**: Comprehensive URL and input validation
- **Error Handling**: Graceful error handling with informative messages
- **Threading**: Non-blocking downloads that don't freeze the UI
- **Safe Downloads**: Automatic filename sanitization for cross-platform compatibility

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer) or uv (fast Python package manager)

### Method 1: Using uv (Recommended - Fast & Modern)

1. **Install uv (if not already installed):**
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or using pip
   pip install uv
   ```

2. **Clone and setup the project:**
   ```bash
   git clone https://github.com/sshussh/python-gui-yt-video-downloader.git
   cd python-gui-yt-video-downloader
   
   # Create virtual environment and install dependencies
   uv sync
   ```

3. **Run the application:**
   ```bash
   uv run python main.py
   ```

### Method 2: Using pip (Traditional)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sshussh/python-gui-yt-video-downloader.git
   cd python-gui-yt-video-downloader
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Dependencies
- `customtkinter>=5.2.0` - Modern GUI framework
- `pytube>=15.0.0` - YouTube video download library
- `Pillow>=9.0.0` - Image processing for thumbnails

### Why uv?
- **⚡ Lightning Fast**: 10-100x faster than pip for dependency resolution and installation
- **🔒 Reproducible**: Generates `uv.lock` for exact dependency versions across environments
- **🎯 Simple**: Single command (`uv sync`) sets up everything automatically
- **🔄 Compatible**: Works alongside pip - you can use either method

## 🚀 Usage

### Basic Usage
1. **Launch the application:**
   ```bash
   python main.py
   ```

2. **Enter YouTube URL:**
   - Paste any valid YouTube URL in the input field
   - Press Enter or click "🔍 Get Info"

3. **Choose your preferences:**
   - **Format**: MP4 (Video) or MP3 (Audio Only)
   - **Quality**: Select from available resolutions
   - **Location**: Choose download folder (defaults to Downloads)

4. **Download:**
   - Click "⬇️ Download" to start
   - Monitor progress in real-time
   - Get notified when complete

### Supported URL Formats
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

## 🎨 Interface Overview

### Header Section
- **🎬 App Title**: Clear branding and identification
- **🌙/☀️ Theme Toggle**: Switch between dark and light modes
- **ℹ️ Info Button**: Access help and application information

### Main Content
- **📎 URL Input**: Large, clear input field for YouTube URLs
- **🔍 Get Info**: Fetch video details and thumbnail
- **📱 Format Selection**: Choose between video and audio formats
- **🎯 Quality Options**: Select resolution/bitrate
- **📁 Download Location**: Browse and select destination folder

### Video Information Panel
- **🖼️ Thumbnail**: Visual preview of the video
- **📹 Title & Details**: Video title, author, duration, and view count
- **📥 Progress Tracking**: Real-time download progress with detailed stats
- **⬇️ Download Button**: Start the download process

## 🛠️ Technical Details

### Architecture
- **GUI Framework**: CustomTkinter for modern, cross-platform interface
- **Download Engine**: PyTube for reliable YouTube video downloading
- **Threading**: Asynchronous operations to maintain UI responsiveness
- **Image Processing**: PIL/Pillow for thumbnail display

### File Structure
```
python-gui-yt-video-downloader/
├── main.py              # Complete application (single file)
├── requirements.txt     # Pip dependencies (legacy)
├── pyproject.toml       # Modern Python project configuration (uv/pip)
├── uv.lock             # Exact dependency versions (uv)
├── .venv/              # Virtual environment (created by uv)
├── assets/             # UI assets
│   └── info_icon.png   # Info button icon
└── README.md           # This file
```

### Key Classes
- `App`: Main application window and logic
- `InfoWindow`: About/help dialog window

## ⚠️ Important Notes

### Legal Compliance
- **Respect Copyright**: Only download content you have permission to download
- **YouTube ToS**: Ensure compliance with YouTube's Terms of Service
- **Personal Use**: This tool is intended for personal, educational use only

### Limitations
- **Format Conversion**: MP3 extraction is basic (full conversion requires FFmpeg)
- **Playlist Support**: Currently supports single videos only
- **Live Streams**: Live or premiering videos may not be downloadable

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

#### Using uv (Recommended)
1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/python-gui-yt-video-downloader.git`
3. Navigate to directory: `cd python-gui-yt-video-downloader`
4. Install dependencies: `uv sync`
5. Create a feature branch: `git checkout -b feature/AmazingFeature`
6. Make your changes
7. Test the application: `uv run python main.py`
8. Commit your changes: `git commit -m 'Add some AmazingFeature'`
9. Push to the branch: `git push origin feature/AmazingFeature`
10. Open a Pull Request

#### Using pip (Traditional)
1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/python-gui-yt-video-downloader.git`
3. Navigate to directory: `cd python-gui-yt-video-downloader`
4. Create virtual environment: `python -m venv venv`
5. Activate virtual environment: 
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
6. Install dependencies: `pip install -r requirements.txt`
7. Create a feature branch: `git checkout -b feature/AmazingFeature`
8. Make your changes
9. Test the application: `python main.py`
10. Commit your changes: `git commit -m 'Add some AmazingFeature'`
11. Push to the branch: `git push origin feature/AmazingFeature`
12. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**"No module named 'tkinter'"**
- Install tkinter: `sudo apt-get install python3-tk` (Linux)
- tkinter is included with Python on Windows/macOS

**"SSL Certificate Error"**
- Update certificates or try with `--trusted-host` pip flag

**"Download Failed"**
- Check internet connection
- Verify the YouTube URL is accessible
- Some videos may be region-restricted or age-gated

**"Permission Denied"**
- Ensure write permissions for the download directory
- Try running as administrator (Windows) or with sudo (Linux/macOS)

### Getting Help
- Check existing issues on GitHub
- Create a new issue with detailed error information
- Include your Python version and operating system

## 🌟 Acknowledgments

- **CustomTkinter**: For the beautiful, modern GUI framework
- **PyTube**: For reliable YouTube downloading capabilities
- **Python Community**: For the excellent ecosystem of libraries

---

**Made with ❤️ using Python & CustomTkinter**

*Enjoy downloading your favorite YouTube content responsibly!* 🎉