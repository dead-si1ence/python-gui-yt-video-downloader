import os
import threading
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as tkmb
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

        self.__InitUi__()

    def __InitUi__(self):
        self.info = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

        self.infoTextbox = ctk.CTkTextbox(self, wrap="word")
        self.infoTextbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.infoTextbox.insert(tk.CURRENT, self.info)
        self.infoTextbox.configure(state="disabled")

        self.closeButton = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.closeButton.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)


class App(ctk.CTk):
    """The main application window for the Youtube Downloader.

    Args:
        ctk (_type_): _description_
    """
    def __init__(self):
        """Initialize the main application window.
        """
        super().__init__()
        self.title("Youtube Downloader")
        self.geometry("600x350")
        self.resizable(False, False)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.__InitUi__()

        self.downloadThread = None

    def __InitUi__(self):
        """Initialize the UI components.
        
        This method initializes the UI components of the application.
        """
        self.mainLabelFrame = ctk.CTkFrame(self)
        self.mainLabelFrame.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew"
        )
        self.mainLabelFrame.grid_columnconfigure(0, weight=1)
        self.mainLabelFrame.grid_columnconfigure(1, weight=0)

        self.mainLabel = ctk.CTkLabel(
            self.mainLabelFrame, text="Youtube Video Downloader", font=("Arial", 20)
        )
        self.mainLabel.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        self.infoButtonImageImage = Image.open(
            r"d:\dev\python\Projects\YouTubeVideoDownloader\assets\info_icon.png"
        )
        self.infoButtonImage = ctk.CTkImage(
            light_image=self.infoButtonImageImage,
            dark_image=self.infoButtonImageImage,
            size=(25, 25),
        )

        self.infoButton = ctk.CTkButton(
            self.mainLabelFrame,
            width=25,
            height=25,
            text="",
            image=self.infoButtonImage,
            command=self.InfoButtonEventHandler,
        )
        self.infoButton.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.grid(row=1, column=0, padx=(10, 10), pady=(5, 10), sticky="nsew")
        self.mainFrame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.mainFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.enterUrlLabel = ctk.CTkLabel(self.mainFrame, text="Enter URL:")
        self.enterUrlLabel.grid(row=0, column=0, sticky="n", padx=20, pady=10)

        self.enterUrlEntry = ctk.CTkEntry(
            self.mainFrame, width=450, placeholder_text="URL..."
        )
        self.enterUrlEntry.grid(
            row=0, column=1, columnspan=3, sticky="n", padx=10, pady=10
        )

        self.videoTitleLabel = ctk.CTkLabel(self.mainFrame, text="Video Title:")
        self.videoTitleLabel.grid(row=1, column=0, sticky="n", padx=10, pady=10)

        self.videoTitleTitleLabel = ctk.CTkLabel(self.mainFrame, text="")
        self.videoTitleTitleLabel.grid(
            row=1, column=1, columnspan=3, sticky="n", padx=10, pady=10
        )

        self.selectResolutionLabel = ctk.CTkLabel(self.mainFrame, text="Resolution:")
        self.selectResolutionLabel.grid(row=2, column=0, sticky="n", padx=10, pady=10)

        self.selectResolutionComboBox = ctk.CTkComboBox(
            self.mainFrame, values=["720p", "1080p", "1440p", "2160p"]
        )
        self.selectResolutionComboBox.grid(
            row=2, column=1, sticky="n", padx=10, pady=10
        )

        self.selectDownloadPathLabel = ctk.CTkLabel(
            self.mainFrame, text="Download Path:"
        )
        self.selectDownloadPathLabel.grid(row=2, column=2, sticky="n", padx=10, pady=10)

        self.selectDownloadPathButton = ctk.CTkButton(
            self.mainFrame,
            text="Browse...",
            command=self.SelectDownloadPathButtonEventHandler,
        )
        self.selectDownloadPathButton.grid(
            row=2, column=3, sticky="n", padx=10, pady=10
        )

        self.getInfoButton = ctk.CTkButton(
            self.mainFrame, text="Get Info", command=self.GetInfoButtonEventHandler
        )
        self.getInfoButton.grid(row=3, column=0, sticky="s", padx=10, pady=10)

        self.downloadButton = ctk.CTkButton(
            self.mainFrame, text="Download", command=self.DownloadButtonEventHandler
        )
        self.downloadButton.grid(row=3, column=1, sticky="s", padx=10, pady=10)

        self.downloadProgressBar = ctk.CTkProgressBar(
            self.mainFrame, orientation="horozontal", mode="determinate"
        )
        self.downloadProgressBar.grid(
            row=3, column=2, columnspan=2, sticky="s", padx=10, pady=(10, 20)
        )
        self.downloadProgressBar.set(0)

    def InfoButtonEventHandler(self):
        """Show the info window.
        """
        self.InfoWindow = InfoWindow()
        self.InfoWindow.focus_set()

    def GetInfoButtonEventHandler(self):
        """Get the video information and set the title label.
        """
        self.url = self.enterUrlEntry.get()
        self.video = pt.YouTube(
            self.url, on_progress_callback=self.DownloadProgressBarSet
        )
        self.title = self.video.title

        self.videoTitleTitleLabel.configure(text=self.title)

    def DownloadButtonEventHandler(self):
        """Start the download thread.
        """
        if self.downloadThread is None or not self.downloadThread.is_alive():
            self.downloadThread = threading.Thread(target=self.DownloadVideo)
            self.downloadThread.start()

    def DownloadVideo(self):
        """Download the video to the selected download path.
        """
        try:
            self.video.streams.get_highest_resolution().download(
                output_path=self.downloadPath
            )
        except Exception as e:
            print(f"Download failed: {e}")

    def SelectDownloadPathButtonEventHandler(self):
        """Open a file dialog to select the download path.
        """
        self.downloadPath = ctk.filedialog.askdirectory(initialdir=os.getcwd())

    def DownloadProgressBarSet(self, stream, _, bytes_remaining):
        """Set the progress bar value based on the download progress.

        Args:
            stream (Stream): The stream object of the video.
            _ (Chunk): The chunk of the video.
            bytes_remaining (int): The number of bytes remaining to download.
        """
        self.total_size = stream.filesize
        self.bytes_downloaded = self.total_size - bytes_remaining
        self.percentage = int((self.bytes_downloaded / self.total_size) * 100) / 100
        self.downloadProgressBar.set(self.percentage)
        # creat a pop up window to show the download progress when the download is finished
        if self.percentage == 1:
            self.ShowDownloadCompletePopup()

    def ShowDownloadCompletePopup(self):
        """Show a popup window when the download is complete.
        """
        tkmb.showinfo(
            title="Download Complete",
            message="The video has been downloaded successfully!",
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
