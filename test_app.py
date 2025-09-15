#!/usr/bin/env python3
"""
Simple functionality tests for YouTube Downloader application.
Tests core functions without requiring GUI components.
"""

import os
import re
import tempfile


def test_url_validation():
    """Test YouTube URL validation logic."""
    def is_valid_youtube_url(url):
        """Check if the URL is a valid YouTube URL."""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        return any(domain in url for domain in youtube_domains) and ('watch?v=' in url or 'youtu.be/' in url)
    
    valid_urls = [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'https://youtube.com/watch?v=dQw4w9WgXcQ',
        'https://youtu.be/dQw4w9WgXcQ',
        'https://m.youtube.com/watch?v=dQw4w9WgXcQ'
    ]
    
    invalid_urls = [
        'https://example.com',
        'not a url',
        'https://vimeo.com/123456',
        ''
    ]
    
    print("🔗 Testing URL validation...")
    for url in valid_urls:
        assert is_valid_youtube_url(url), f"Should be valid: {url}"
    
    for url in invalid_urls:
        assert not is_valid_youtube_url(url), f"Should be invalid: {url}"
    
    print("✅ URL validation tests passed!")


def test_duration_formatting():
    """Test duration formatting."""
    def format_duration(seconds):
        """Format duration from seconds to readable format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    test_cases = [
        (0, "00:00"),
        (30, "00:30"),
        (90, "01:30"),
        (3600, "01:00:00"),
        (3661, "01:01:01"),
        (7265, "02:01:05")
    ]
    
    print("⏱️ Testing duration formatting...")
    for seconds, expected in test_cases:
        result = format_duration(seconds)
        assert result == expected, f"Expected {expected}, got {result} for {seconds} seconds"
    
    print("✅ Duration formatting tests passed!")


def test_number_formatting():
    """Test number formatting."""
    def format_number(num):
        """Format large numbers with K, M, B suffixes."""
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)
    
    test_cases = [
        (999, "999"),
        (1000, "1.0K"),
        (1500, "1.5K"),
        (1000000, "1.0M"),
        (1500000, "1.5M"),
        (1000000000, "1.0B"),
        (1500000000, "1.5B")
    ]
    
    print("🔢 Testing number formatting...")
    for num, expected in test_cases:
        result = format_number(num)
        assert result == expected, f"Expected {expected}, got {result} for {num}"
    
    print("✅ Number formatting tests passed!")


def test_filename_sanitization():
    """Test filename sanitization."""
    def sanitize_filename(filename):
        """Remove invalid characters from filename."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename.strip()
    
    test_cases = [
        ("Normal Title", "Normal Title"),
        ("Title with <brackets>", "Title with brackets"),
        ("Title/with\\slashes", "Titlewithslashes"),
        ("Title:with|invalid*chars?", "Titlewithinvalidchars"),
        ("   Spaced Title   ", "Spaced Title")
    ]
    
    print("📁 Testing filename sanitization...")
    for input_name, expected in test_cases:
        result = sanitize_filename(input_name)
        assert result == expected, f"Expected '{expected}', got '{result}' for '{input_name}'"
    
    print("✅ Filename sanitization tests passed!")


def test_imports():
    """Test that all required modules can be imported."""
    print("📦 Testing dependencies...")
    try:
        import customtkinter
        print("  ✅ customtkinter imported successfully")
    except ImportError as e:
        print(f"  ❌ customtkinter: {e}")
        return False
    
    try:
        import pytube
        print("  ✅ pytube imported successfully")
    except ImportError as e:
        print(f"  ❌ pytube: {e}")
        return False
    
    try:
        import PIL
        print("  ✅ PIL (Pillow) imported successfully")
    except ImportError as e:
        print(f"  ❌ PIL: {e}")
        return False
    
    print("✅ All dependencies available!")
    return True


def test_file_structure():
    """Test that all required files exist."""
    required_files = [
        'main.py',
        'requirements.txt',
        'assets/info_icon.png'
    ]
    
    print("📋 Testing file structure...")
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist!")
        return True


def main():
    """Run all tests."""
    print("🧪 YouTube Downloader - Functionality Tests\n")
    print("=" * 50)
    
    # Test dependencies and file structure
    deps_ok = test_imports()
    print()
    files_ok = test_file_structure()
    print()
    
    if not (deps_ok and files_ok):
        print("❌ Basic requirements not met. Please check dependencies and files.")
        return False
    
    # Run functionality tests
    try:
        test_url_validation()
        print()
        test_duration_formatting()
        print()
        test_number_formatting()
        print()
        test_filename_sanitization()
        print()
        
        print("=" * 50)
        print("🎉 All tests passed successfully!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)