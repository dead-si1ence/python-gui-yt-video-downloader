#!/usr/bin/env python3
"""
Example script demonstrating YouTube Downloader core functionality.
This script works without GUI to show the download capabilities.
"""

import os
import sys
from urllib.parse import urlparse, parse_qs

# Mock the GUI-dependent parts for demonstration
class MockYouTubeDownloader:
    """Mock YouTube downloader that demonstrates core functionality."""
    
    def __init__(self):
        self.download_path = os.path.expanduser("~/Downloads")
    
    def is_valid_youtube_url(self, url):
        """Check if the URL is a valid YouTube URL."""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        return any(domain in url for domain in youtube_domains) and ('watch?v=' in url or 'youtu.be/' in url)
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename.strip()
    
    def format_duration(self, seconds):
        """Format duration from seconds to readable format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def format_number(self, num):
        """Format large numbers with K, M, B suffixes."""
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)
    
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL."""
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        elif 'watch?v=' in url:
            parsed = urlparse(url)
            return parse_qs(parsed.query)['v'][0]
        return None
    
    def simulate_download(self, url, format_type="MP4", quality="720p"):
        """Simulate a download operation."""
        print(f"🎬 YouTube Downloader - Core Functionality Demo")
        print("=" * 50)
        
        # Validate URL
        if not self.is_valid_youtube_url(url):
            print("❌ Invalid YouTube URL!")
            return False
        
        print(f"✅ Valid YouTube URL detected")
        
        # Extract video ID
        video_id = self.extract_video_id(url)
        print(f"📺 Video ID: {video_id}")
        
        # Simulate video info
        mock_title = "Sample Video Title - Amazing Content!"
        mock_duration = 245  # 4:05
        mock_views = 1234567
        mock_author = "Content Creator"
        
        sanitized_title = self.sanitize_filename(mock_title)
        formatted_duration = self.format_duration(mock_duration)
        formatted_views = self.format_number(mock_views)
        
        print(f"\n📹 Video Information:")
        print(f"   Title: {mock_title}")
        print(f"   Sanitized: {sanitized_title}")
        print(f"   Author: {mock_author}")
        print(f"   Duration: {formatted_duration}")
        print(f"   Views: {formatted_views}")
        
        # Simulate download settings
        print(f"\n⚙️  Download Settings:")
        print(f"   Format: {format_type}")
        print(f"   Quality: {quality}")
        print(f"   Path: {self.download_path}")
        
        # Simulate filename
        if format_type == "MP3":
            filename = f"{sanitized_title}.mp3"
        else:
            filename = f"{sanitized_title}.mp4"
        
        full_path = os.path.join(self.download_path, filename)
        print(f"   Full path: {full_path}")
        
        # Simulate progress
        print(f"\n📥 Simulating Download Progress:")
        for i in range(0, 101, 20):
            print(f"   Progress: {i}% {'█' * (i//10)}")
        
        print(f"\n✅ Download completed successfully!")
        print(f"🎉 File saved as: {filename}")
        
        return True


def main():
    """Demonstrate the YouTube downloader functionality."""
    downloader = MockYouTubeDownloader()
    
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://invalid-url.com",
    ]
    
    print("🧪 Testing URL Validation:")
    for url in test_urls:
        is_valid = downloader.is_valid_youtube_url(url)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {url}")
    
    print("\n" + "=" * 60)
    
    # Simulate a download
    valid_url = test_urls[0]
    downloader.simulate_download(valid_url, "MP4", "1080p")
    
    print("\n" + "=" * 60)
    print("💡 This is a demonstration of core functionality.")
    print("   Run 'python main.py' for the full GUI application!")


if __name__ == "__main__":
    main()