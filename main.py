import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import pytube as pt


class InfoWindow(ctk.CTkToplevel):
    """A custom top-level window for displaying information."""

    def __init__(self):
        super().__init__()
        self.title("Info")
        self.geometry("300x350")
        self.resizable(False, False)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.__init_ui__()

    def __init_ui__(self):
        self.info = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad "
            "minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip "
            "ex ea commodo consequat. Duis aute irure dolor in reprehenderit in "
            "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur "
            "sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
            "mollit anim id est laborum."
        )

        self.info_textbox = ctk.CTkTextbox(self, wrap="word")
        self.info_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.info_textbox.insert(tk.CURRENT, self.info)
        self.info_textbox.configure(state="disabled")

        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)


class App(ctk.CTk):
    """The main application window for the YouTube Downloader."""

    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("600x350")
        self.resizable(False, False)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.__init_ui__()
        self.download_thread = None

    def __init_ui__(self):
        self.main_label_frame = ctk.CTkFrame(self)
        self.main_label_frame.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew"
        )
        self.main_label_frame.grid_columnconfigure(0, weight=1)
        self.main_label_frame.grid_columnconfigure(1, weight=0)

        self.main_label = ctk.CTkLabel(
            self.main_label_frame, text="YouTube Video Downloader", font=("Arial", 20)
        )
        self.main_label.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        image_path = os.path.join(
            os.path.dirname(__file__), "assets", "info_icon.png"
        )
        self.info_button_image = ctk.CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(25, 25),
        )

        self.info_button = ctk.CTkButton(
            self.main_label_frame,
            width=25,
            height=25,
            text="",
            image=self.info_button_image,
            command=self.info_button_event_handler,
        )
        self.info_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=(10, 10), pady=(5, 10), sticky="nsew")
        self.main_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.enter_url_label = ctk.CTkLabel(self.main_frame, text="Enter URL:")
        self.enter_url_label.grid(row=0, column=0, sticky="n", padx=20, pady=10)

        self.enter_url_entry = ctk.CTkEntry(
            self.main_frame, width=450, placeholder_text="URL..."
        )
        self.enter_url_entry.grid(
            row=0, column=1, columnspan=3, sticky="n", padx=10, pady=10
        )

        self.video_title_label = ctk.CTkLabel(self.main_frame, text="Video Title:")
        self.video_title_label.grid(row=1, column=0, sticky="n", padx=10, pady=10)

        self.video_title_title_label = ctk.CTkLabel(self.main_frame, text="")
        self.video_title_title_label.grid(
            row=1, column=1, columnspan=3, sticky="n", padx=10, pady=10
        )

        self.select_resolution_label = ctk.CTkLabel(self.main_frame, text="Resolution:")
        self.select_resolution_label.grid(row=2, column=0, sticky="n", padx=10, pady=10)

        self.select_resolution_combo_box = ctk.CTkComboBox(
            self.main_frame, values=["720p", "1080p", "1440p", "2160p"]
        )
        self.select_resolution_combo_box.grid(
            row=2, column=1, sticky="n", padx=10, pady=10
        )

        self.select_download_path_label = ctk.CTkLabel(
            self.main_frame, text="Download Path:"
        )
        self.select_download_path_label.grid(row=2, column=2, sticky="n", padx=10, pady=10)

        self.select_download_path_button = ctk.CTkButton(
            self.main_frame,
            text="Browse...",
            command=self.select_download_path_button_event_handler,
        )
        self.select_download_path_button.grid(
            row=2, column=3, sticky="n", padx=10, pady=10
        )

        self.get_info_button = ctk.CTkButton(
            self.main_frame, text="Get Info", command=self.get_info_button_event_handler
        )
        self.get_info_button.grid(row=3, column=0, sticky="s", padx=10, pady=10)

        self.download_button = ctk.CTkButton(
            self.main_frame, text="Download", command=self.download_button_event_handler
        )
        self.download_button.grid(row=3, column=1, sticky="s", padx=10, pady=10)

        self.download_progress_bar = ctk.CTkProgressBar(
            self.main_frame, orientation="horizontal", mode="determinate"
        )
        self.download_progress_bar.grid(
            row=3, column=2, columnspan=2, sticky="s", padx=10, pady=(10, 20)
        )
        self.download_progress_bar.set(0)

    def info_button_event_handler(self):
        """Show the info window."""
        info_window = InfoWindow()
        info_window.focus_set()

    def get_info_button_event_handler(self):
        """Get the video information and set the title label."""
        self.url = self.enter_url_entry.get()
        try:
            self.video = pt.YouTube(
                self.url, on_progress_callback=self.download_progress_bar_set
            )
            self.title = self.video.title
            self.video_title_title_label.configure(text=self.title)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve video info: {e}")

    def download_button_event_handler(self):
        """Start the download thread."""
        if self.download_thread is None or not self.download_thread.is_alive():
            self.download_thread = threading.Thread(target=self.download_video)
            self.download_thread.start()

    def download_video(self):
        """Download the video to the selected download path."""
        try:
            stream = self.video.streams.get_highest_resolution()
            stream.download(output_path=self.download_path)
            self.show_download_complete_popup()
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")

    def select_download_path_button_event_handler(self):
        """Open a file dialog to select the download path."""
        self.download_path = filedialog.askdirectory(initialdir=os.getcwd())

    def download_progress_bar_set(self, stream, _, bytes_remaining):
        """Set the progress bar value based on the download progress."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        self.download_progress_bar.set(percentage)
        if percentage == 1.0:
            self.show_download_complete_popup()

    def show_download_complete_popup(self):
        """Show a popup window when the download is complete."""
        messagebox.showinfo(
            title="Download Complete",
            message="The video has been downloaded successfully!",
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
