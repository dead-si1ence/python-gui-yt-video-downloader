import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import pytube as pt
import json
from urllib.request import urlopen
import tempfile


class InfoWindow(ctk.CTkToplevel):
    """A custom top-level window for displaying application information."""

    def __init__(self):
        super().__init__()
        self.title("About YouTube Downloader")
        self.geometry("400x500")
        self.resizable(False, False)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.__init_ui__()

    def __init_ui__(self):
        self.info = (
            "🎬 YouTube Video Downloader v2.0\n\n"
            "A modern, user-friendly application for downloading YouTube videos "
            "with support for multiple formats and resolutions.\n\n"
            "✨ Features:\n"
            "• Download videos in multiple resolutions (360p to 4K)\n"
            "• Support for MP4 video and MP3 audio formats\n"
            "• Real-time download progress tracking\n"
            "• Video thumbnail preview\n"
            "• Customizable download location\n"
            "• Modern dark/light theme interface\n\n"
            "🔧 How to use:\n"
            "1. Paste a YouTube URL in the input field\n"
            "2. Click 'Get Info' to fetch video details\n"
            "3. Select your preferred quality and format\n"
            "4. Choose download location\n"
            "5. Click 'Download' to start\n\n"
            "⚠️ Legal Notice:\n"
            "Please respect copyright laws and YouTube's Terms of Service. "
            "Only download content you have permission to download.\n\n"
            "Made with ❤️ using Python & CustomTkinter"
        )

        self.info_textbox = ctk.CTkTextbox(self, wrap="word", font=("Arial", 12))
        self.info_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.info_textbox.insert(tk.CURRENT, self.info)
        self.info_textbox.configure(state="disabled")

        self.close_button = ctk.CTkButton(
            self, text="Close", command=self.destroy, 
            font=("Arial", 12, "bold"), height=40
        )
        self.close_button.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))


class App(ctk.CTk):
    """The main application window for the YouTube Downloader."""

    def __init__(self):
        super().__init__()
        # Set theme and appearance
        ctk.set_appearance_mode("system")  # or "light", "dark"
        ctk.set_default_color_theme("blue")  # or "green", "dark-blue"
        
        self.title("🎬 YouTube Video Downloader")
        self.geometry("800x600")
        self.resizable(True, True)
        self.minsize(700, 500)
        
        # Configure grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize variables
        self.video = None
        self.download_thread = None
        self.download_path = os.path.expanduser("~/Downloads")
        self.available_streams = []
        self.thumbnail_image = None
        
        self.__init_ui__()

    def __init_ui__(self):
        # Header frame
        self.header_frame = ctk.CTkFrame(self, height=80)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=1)

        # Title and info button container
        self.title_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.title_container.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        self.title_container.grid_columnconfigure(0, weight=1)

        self.main_label = ctk.CTkLabel(
            self.title_container, 
            text="🎬 YouTube Video Downloader", 
            font=("Arial", 24, "bold")
        )
        self.main_label.grid(row=0, column=0, sticky="w")

        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            self.title_container,
            text="🌙",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.toggle_theme
        )
        self.theme_button.grid(row=0, column=1, padx=(10, 0), sticky="e")

        # Info button
        self.info_button = ctk.CTkButton(
            self.title_container,
            text="ℹ️",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.info_button_event_handler
        )
        self.info_button.grid(row=0, column=2, padx=(5, 0), sticky="e")

        # Main content frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(3, weight=1)  # Make video info frame expandable
        self.main_frame.grid_columnconfigure(1, weight=1)

        # URL input section
        self.url_label = ctk.CTkLabel(self.main_frame, text="📎 YouTube URL:", font=("Arial", 14, "bold"))
        self.url_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.url_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.url_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            self.url_frame,
            placeholder_text="Paste YouTube URL here...",
            font=("Arial", 12),
            height=40
        )
        self.url_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.url_entry.bind("<Return>", lambda e: self.get_info_button_event_handler())

        self.get_info_button = ctk.CTkButton(
            self.url_frame,
            text="🔍 Get Info",
            width=120,
            height=40,
            font=("Arial", 12, "bold"),
            command=self.get_info_button_event_handler
        )
        self.get_info_button.grid(row=0, column=1)

        # Download options frame
        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.options_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Format selection
        self.format_label = ctk.CTkLabel(self.options_frame, text="📱 Format:", font=("Arial", 12, "bold"))
        self.format_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.format_combo = ctk.CTkComboBox(
            self.options_frame,
            values=["MP4 (Video)", "MP3 (Audio Only)"],
            font=("Arial", 11),
            state="readonly",
            command=self.format_changed
        )
        self.format_combo.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        self.format_combo.set("MP4 (Video)")

        # Quality selection
        self.quality_label = ctk.CTkLabel(self.options_frame, text="🎯 Quality:", font=("Arial", 12, "bold"))
        self.quality_label.grid(row=0, column=1, padx=20, pady=(15, 5), sticky="w")

        self.quality_combo = ctk.CTkComboBox(
            self.options_frame,
            values=["Best Available"],
            font=("Arial", 11),
            state="readonly"
        )
        self.quality_combo.grid(row=1, column=1, padx=20, pady=(0, 15), sticky="ew")
        self.quality_combo.set("Best Available")

        # Download path selection
        self.path_label = ctk.CTkLabel(self.options_frame, text="📁 Download to:", font=("Arial", 12, "bold"))
        self.path_label.grid(row=0, column=2, padx=20, pady=(15, 5), sticky="w")

        self.path_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.path_frame.grid(row=1, column=2, padx=20, pady=(0, 15), sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.path_display = ctk.CTkLabel(
            self.path_frame,
            text=f"📂 {os.path.basename(self.download_path)}",
            font=("Arial", 10),
            anchor="w"
        )
        self.path_display.grid(row=0, column=0, sticky="ew")

        self.browse_button = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            width=70,
            height=30,
            font=("Arial", 10),
            command=self.select_download_path_button_event_handler
        )
        self.browse_button.grid(row=0, column=1, padx=(5, 0))

        # Video info frame
        self.video_info_frame = ctk.CTkFrame(self.main_frame)
        self.video_info_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
        self.video_info_frame.grid_columnconfigure(1, weight=1)
        self.video_info_frame.grid_rowconfigure(1, weight=1)

        # Thumbnail placeholder
        self.thumbnail_label = ctk.CTkLabel(
            self.video_info_frame,
            text="🖼️\nThumbnail\nwill appear\nhere",
            width=160,
            height=120,
            font=("Arial", 12),
            corner_radius=8
        )
        self.thumbnail_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nw")

        # Video details
        self.details_frame = ctk.CTkFrame(self.video_info_frame, fg_color="transparent")
        self.details_frame.grid(row=0, column=1, padx=(0, 20), pady=(20, 10), sticky="ew")
        self.details_frame.grid_columnconfigure(0, weight=1)

        self.video_title = ctk.CTkLabel(
            self.details_frame,
            text="📹 Video title will appear here after getting info",
            font=("Arial", 14, "bold"),
            anchor="w",
            wraplength=400
        )
        self.video_title.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.video_stats = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=("Arial", 11),
            anchor="w"
        )
        self.video_stats.grid(row=1, column=0, sticky="ew")

        # Download controls frame
        self.download_frame = ctk.CTkFrame(self.video_info_frame, fg_color="transparent")
        self.download_frame.grid(row=1, column=1, padx=(0, 20), pady=(0, 20), sticky="sew")
        self.download_frame.grid_columnconfigure(0, weight=1)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.download_frame, height=20)
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.progress_bar.set(0)

        # Progress label
        self.progress_label = ctk.CTkLabel(
            self.download_frame,
            text="Ready to download",
            font=("Arial", 11)
        )
        self.progress_label.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Download button
        self.download_button = ctk.CTkButton(
            self.download_frame,
            text="⬇️ Download",
            height=40,
            font=("Arial", 14, "bold"),
            command=self.download_button_event_handler,
            state="disabled"
        )
        self.download_button.grid(row=2, column=0, sticky="ew")

    def toggle_theme(self):
        """Toggle between dark and light themes."""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="🌙")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="☀️")

    def info_button_event_handler(self):
        """Show the info window."""
        info_window = InfoWindow()
        info_window.focus_set()

    def format_changed(self, choice):
        """Handle format selection change."""
        self.update_quality_options()

    def update_quality_options(self):
        """Update quality options based on format selection and available streams."""
        if not self.available_streams:
            return

        format_choice = self.format_combo.get()
        if "MP3" in format_choice:
            # For audio, show audio quality options
            qualities = ["128 kbps", "192 kbps", "256 kbps", "320 kbps"]
        else:
            # For video, show available resolutions
            video_streams = [s for s in self.available_streams if s.mime_type.startswith('video')]
            resolutions = list(set([s.resolution for s in video_streams if s.resolution]))
            
            # Sort resolutions by quality (rough sorting)
            quality_order = ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p']
            qualities = sorted(resolutions, key=lambda x: quality_order.index(x) if x in quality_order else 999)
            
            if not qualities:
                qualities = ["Best Available"]

        self.quality_combo.configure(values=qualities)
        if qualities:
            self.quality_combo.set(qualities[-1])  # Set to highest quality by default

    def get_info_button_event_handler(self):
        """Get video information and populate the UI."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        # Disable button and show loading
        self.get_info_button.configure(text="🔍 Loading...", state="disabled")
        self.progress_label.configure(text="Fetching video information...")
        
        # Use threading to prevent UI freeze
        thread = threading.Thread(target=self._fetch_video_info, args=(url,))
        thread.daemon = True
        thread.start()

    def is_valid_youtube_url(self, url):
        """Check if the URL is a valid YouTube URL."""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        return any(domain in url for domain in youtube_domains) and ('watch?v=' in url or 'youtu.be/' in url)

    def _fetch_video_info(self, url):
        """Fetch video information in a separate thread."""
        try:
            self.video = pt.YouTube(url, on_progress_callback=self.download_progress_callback)
            self.available_streams = self.video.streams.filter(adaptive=True, file_extension='mp4')
            
            # Update UI in main thread
            self.after(0, self._update_video_info)
            
        except Exception as e:
            # Show error in main thread
            self.after(0, lambda: self._show_fetch_error(str(e)))

    def _update_video_info(self):
        """Update the UI with video information."""
        try:
            # Update video title
            title = self.video.title
            if len(title) > 60:
                title = title[:57] + "..."
            self.video_title.configure(text=f"📹 {title}")

            # Update video stats
            duration = self.format_duration(self.video.length)
            views = self.format_number(self.video.views)
            author = self.video.author
            
            stats_text = f"👤 {author}\n⏱️ Duration: {duration}\n👀 Views: {views}"
            self.video_stats.configure(text=stats_text)

            # Load thumbnail
            self.load_thumbnail()

            # Update quality options
            self.update_quality_options()

            # Enable download button
            self.download_button.configure(state="normal")
            self.progress_label.configure(text="Ready to download")

        except Exception as e:
            self._show_fetch_error(f"Error updating video info: {str(e)}")
        finally:
            # Re-enable get info button
            self.get_info_button.configure(text="🔍 Get Info", state="normal")

    def _show_fetch_error(self, error_msg):
        """Show error message and reset UI."""
        messagebox.showerror("Error", f"Failed to fetch video information:\n{error_msg}")
        self.get_info_button.configure(text="🔍 Get Info", state="normal")
        self.progress_label.configure(text="Ready to get video info")

    def format_duration(self, seconds):
        """Format duration from seconds to readable format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

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

    def load_thumbnail(self):
        """Load and display video thumbnail."""
        try:
            # Get thumbnail URL
            thumbnail_url = self.video.thumbnail_url
            
            # Download thumbnail in a separate thread
            thread = threading.Thread(target=self._download_thumbnail, args=(thumbnail_url,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            print(f"Error loading thumbnail: {e}")

    def _download_thumbnail(self, thumbnail_url):
        """Download thumbnail image."""
        try:
            # Download thumbnail
            with urlopen(thumbnail_url) as response:
                thumbnail_data = response.read()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(thumbnail_data)
                temp_path = temp_file.name
            
            # Update UI in main thread
            self.after(0, lambda: self._display_thumbnail(temp_path))
            
        except Exception as e:
            print(f"Error downloading thumbnail: {e}")

    def _display_thumbnail(self, image_path):
        """Display the thumbnail image."""
        try:
            # Load and resize image
            image = Image.open(image_path)
            image = image.resize((160, 120), Image.Resampling.LANCZOS)
            
            # Convert to CTkImage
            self.thumbnail_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(160, 120)
            )
            
            # Update label
            self.thumbnail_label.configure(image=self.thumbnail_image, text="")
            
            # Clean up temp file
            try:
                os.unlink(image_path)
            except:
                pass
                
        except Exception as e:
            print(f"Error displaying thumbnail: {e}")

    def download_button_event_handler(self):
        """Start the download process."""
        if not self.video:
            messagebox.showerror("Error", "Please get video info first")
            return

        if not self.download_path:
            messagebox.showerror("Error", "Please select a download path")
            return

        # Check if download is already in progress
        if self.download_thread and self.download_thread.is_alive():
            messagebox.showinfo("Info", "Download is already in progress")
            return

        # Disable download button and start download
        self.download_button.configure(text="⏸️ Downloading...", state="disabled")
        self.progress_label.configure(text="Starting download...")
        
        # Start download in separate thread
        self.download_thread = threading.Thread(target=self._download_video)
        self.download_thread.daemon = True
        self.download_thread.start()

    def _download_video(self):
        """Download the video/audio in a separate thread."""
        try:
            format_choice = self.format_combo.get()
            quality_choice = self.quality_combo.get()
            
            if "MP3" in format_choice:
                # Download audio only
                stream = self.video.streams.filter(only_audio=True, file_extension='mp4').first()
                if not stream:
                    stream = self.video.streams.filter(only_audio=True).first()
                
                if stream:
                    # Download and convert to MP3
                    filename = f"{self.sanitize_filename(self.video.title)}.mp3"
                    self.after(0, lambda: self.progress_label.configure(text="Downloading audio..."))
                    
                    # Download audio stream
                    temp_path = stream.download(output_path=self.download_path, filename_prefix="temp_")
                    
                    # For now, just rename to .mp3 (full conversion would require ffmpeg)
                    final_path = os.path.join(self.download_path, filename)
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    os.rename(temp_path, final_path)
                else:
                    raise Exception("No audio stream available")
            else:
                # Download video
                if quality_choice == "Best Available":
                    stream = self.video.streams.get_highest_resolution()
                else:
                    stream = self.video.streams.filter(res=quality_choice, file_extension='mp4').first()
                    if not stream:
                        stream = self.video.streams.filter(res=quality_choice).first()
                    if not stream:
                        stream = self.video.streams.get_highest_resolution()
                
                if stream:
                    filename = f"{self.sanitize_filename(self.video.title)}.mp4"
                    self.after(0, lambda: self.progress_label.configure(text="Downloading video..."))
                    stream.download(output_path=self.download_path, filename=filename)
                else:
                    raise Exception("No video stream available")
            
            # Download completed successfully
            self.after(0, self._download_completed)
            
        except Exception as e:
            # Show error in main thread
            self.after(0, lambda: self._download_failed(str(e)))

    def sanitize_filename(self, filename):
        """Remove invalid characters from filename."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename.strip()

    def _download_completed(self):
        """Handle successful download completion."""
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="✅ Download completed successfully!")
        self.download_button.configure(text="⬇️ Download", state="normal")
        
        messagebox.showinfo(
            "Download Complete",
            f"✅ Video downloaded successfully!\n\n📁 Location: {self.download_path}"
        )

    def _download_failed(self, error_msg):
        """Handle download failure."""
        self.progress_label.configure(text="❌ Download failed")
        self.download_button.configure(text="⬇️ Download", state="normal")
        
        messagebox.showerror(
            "Download Failed",
            f"❌ Failed to download video:\n\n{error_msg}"
        )

    def select_download_path_button_event_handler(self):
        """Open file dialog to select download path."""
        path = filedialog.askdirectory(
            title="Select Download Folder",
            initialdir=self.download_path
        )
        
        if path:
            self.download_path = path
            self.path_display.configure(text=f"📂 {os.path.basename(path)}")

    def download_progress_callback(self, stream, chunk, bytes_remaining):
        """Update progress bar during download."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        
        # Update UI in main thread
        self.after(0, lambda: self._update_progress(percentage, bytes_downloaded, total_size))

    def _update_progress(self, percentage, bytes_downloaded, total_size):
        """Update progress bar and label."""
        self.progress_bar.set(percentage)
        
        # Format file sizes
        downloaded_mb = bytes_downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        
        progress_text = f"📥 Downloading... {downloaded_mb:.1f}/{total_mb:.1f} MB ({percentage*100:.1f}%)"
        self.progress_label.configure(text=progress_text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
