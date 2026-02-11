import os
import shutil
import urllib.parse

import gi
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadCancelled

gi.require_version("Gtk", "4.0")

from gi.repository import (  # noqa: E402
    Gio,  # pyright: ignore[reportMissingModuleSource]
    GLib,  # pyright: ignore[reportMissingModuleSource]
    Gtk,  # pyright: ignore[reportMissingModuleSource]
)


class Downloader:
    def __init__(
        self, url, download_location, format_type, quality, on_progress, cancellable
    ):
        self.url = url
        self.format_type = format_type
        self.quality = quality
        self.download_location = download_location
        self.on_progress = on_progress
        self.cancellable = cancellable

        self._format_options = {
            ("video", "best"): {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
            },
            ("video", "1080p"): {
                "format": "bestvideo[height<=1080]+bestaudio/best",
                "merge_output_format": "mp4",
            },
            ("video", "720p"): {
                "format": "bestvideo[height<=720]+bestaudio/best",
                "merge_output_format": "mp4",
            },
            ("video", "480p"): {
                "format": "bestvideo[height<=480]+bestaudio/best",
                "merge_output_format": "mp4",
            },
            ("audio", "best"): {
                "format": "bestaudio/best",
            },
            ("audio", "m4a"): {
                "format": "bestaudio[ext=m4a]/bestaudio",
                "merge_output_format": "m4a",
            },
            ("audio", "mp3"): {
                "format": "bestaudio/best",
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
                ],
            },
        }

        selected_opts = self._format_options.get((format_type, quality), {})
        self._ydl_opts = {
            **selected_opts,
            "outtmpl": os.path.join(self.download_location, "%(title)s-%(id)s.%(ext)s"),
            "progress_hooks": [self._progress_hook],
        }

    def download(self):
        with YoutubeDL(self._ydl_opts) as ydl:  # pyright: ignore[reportArgumentType]
            ydl.download([self.url])

    def _progress_hook(self, data):
        if self.cancellable and self.cancellable.is_cancelled():
            raise DownloadCancelled()
        if self.on_progress:
            self.on_progress(data)


def _get_downloads_folder():
    """Returns the default downloads path for Windows, macOS, or Linux"""
    home = os.path.expanduser("~")
    downloads_path = os.path.join(home, "Downloads")
    return str(downloads_path)


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.sshussh.YouTubeDownloader")
        GLib.set_application_name("YouTube Downloader")

        self.download_location = _get_downloads_folder()

        self._video_qualities = ["Best", "1080p", "720p", "480p"]
        self._audio_qualities = ["Best", "M4A", "MP3"]
        self._has_ffmpeg = shutil.which("ffmpeg") is not None

        self._download_task = None
        self._cancellable = None

    def do_activate(self):
        window = Gtk.ApplicationWindow(
            application=self,
            title="YouTube Downloader",
        )

        self.window = window

        # region URL entry
        enter_url_label = Gtk.Label(label="Enter URL: ")

        self.url_entry = Gtk.Entry(
            placeholder_text="Paste video URL here...", hexpand=True
        )

        url_box = Gtk.CenterBox(
            orientation=Gtk.Orientation.HORIZONTAL,
            valign=Gtk.Align.START,
        )
        url_box.set_start_widget(enter_url_label)
        url_box.set_end_widget(self.url_entry)
        # endregion

        # region download options
        # region format
        format_type_label = Gtk.Label(label="Format: ")
        self.format_type_drop_down = Gtk.DropDown(
            model=Gtk.StringList().new(["Video", "Audio"])
        )
        self.format_type_drop_down.connect(
            "notify::selected", self._on_format_type_changed
        )
        format_type_box = Gtk.CenterBox(orientation=Gtk.Orientation.HORIZONTAL)
        format_type_box.set_start_widget(format_type_label)
        format_type_box.set_end_widget(self.format_type_drop_down)
        # endregion

        # region quality
        quality_label = Gtk.Label(label="Quality / Format: ")
        # self.quality_drop_down = Gtk.DropDown(model=Gtk.StringList().new(["High", "Low"]))
        self.quality_drop_down = Gtk.DropDown()
        self._set_quality_options("video")
        quality_box = Gtk.CenterBox(orientation=Gtk.Orientation.HORIZONTAL)
        quality_box.set_start_widget(quality_label)
        quality_box.set_end_widget(self.quality_drop_down)
        # endregion

        # region download location
        self.download_location_label = Gtk.Label(
            label=f"Download Location: {self.download_location if self.download_location else ''}"
        )
        self.download_location_button = Gtk.Button(label="Browse")
        self.download_location_button.connect(
            "clicked", lambda x: self._handle_file_dialog()
        )
        download_location_box = Gtk.CenterBox(orientation=Gtk.Orientation.HORIZONTAL)
        download_location_box.set_start_widget(self.download_location_label)
        download_location_box.set_end_widget(self.download_location_button)

        download_options_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10, valign=Gtk.Align.END
        )
        download_options_box.append(format_type_box)
        download_options_box.append(quality_box)
        download_options_box.append(download_location_box)
        # endregion
        # endregion

        # region download
        self.download_button = Gtk.Button(label="Download")
        self.download_button.connect("clicked", lambda x: self._download())
        # endregion

        # region cancel
        self.cancel_button = Gtk.Button(label="Cancel", sensitive=False)
        self.cancel_button.connect("clicked", lambda x: self._cancel_download())
        # endregion

        # region progress bar
        self.status_label = Gtk.Label(label="Idle")
        self.progress_bar = Gtk.ProgressBar(show_text=True, fraction=0.0, text="0%")
        # endregion

        # region content
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_start=10,
            margin_top=10,
            margin_end=10,
            margin_bottom=10,
        )
        content_box.append(url_box)
        content_box.append(download_options_box)
        content_box.append(self.download_button)
        content_box.append(self.cancel_button)
        content_box.append(self.status_label)
        content_box.append(self.progress_bar)

        window.set_child(content_box)
        # endregion

        window.present()

    def _handle_file_dialog(self):
        Gtk.FileDialog(
            title="Select Download Folder",
        ).select_folder(callback=self._handle_file_dialog_finish)

    def _handle_file_dialog_finish(self, dialog, result):
        try:
            self.download_location = dialog.select_folder_finish(result).get_path()
            self.download_location_label.set_label(
                f"Download Location: {self.download_location if self.download_location else ''}"
            )
        except GLib.Error:
            pass

    def _set_busy(self, is_busy):
        self.download_button.set_sensitive(not is_busy)
        self.url_entry.set_sensitive(not is_busy)
        self.format_type_drop_down.set_sensitive(not is_busy)
        self.quality_drop_down.set_sensitive(not is_busy)
        self.download_location_button.set_sensitive(not is_busy)
        self.cancel_button.set_sensitive(is_busy)

    def _on_progress(self, data):
        def _update():
            status = data.get("status")
            if status == "downloading":
                total = data.get("total_bytes") or data.get("total_bytes_estimate")
                downloaded = data.get("downloaded_bytes") or 0
                if total:
                    fraction = min(max(downloaded / total, 0.0), 1.0)
                    self.progress_bar.set_fraction(fraction)
                    self.progress_bar.set_text(f"{fraction * 100:.1f}%")
                else:
                    self.progress_bar.pulse()
                    self.progress_bar.set_text("Downloading...")
                self.status_label.set_text("Downloading...")
            elif status == "finished":
                self.progress_bar.set_fraction(1.0)
                self.progress_bar.set_text("Finalizing...")
                self.status_label.set_text("Finalizing...")
            return False

        GLib.idle_add(_update)

    def _download_worker(
        self, task, cancellable, url, download_location, format_type, quality
    ):
        try:
            downloader = Downloader(
                url,
                download_location,
                format_type,
                quality,
                on_progress=self._on_progress,
                cancellable=cancellable,
            )
            downloader.download()
            task.return_boolean(True)
        except DownloadCancelled:
            task.return_error(GLib.Error(message="Cancelled", domain="yt-dlp", code=2))
        except Exception as e:
            task.return_error(GLib.Error(message=str(e), domain="yt-dlp", code=1))

    def _download_done(self, source_object, result, user_data):
        try:
            result.propagate_boolean()
            self._on_download_complete()
        except GLib.Error as e:
            message = e.message if hasattr(e, "message") else str(e)
            if "Cancelled" in message:
                self._on_download_cancelled()
            else:
                self._on_download_error(message)

    def _on_download_complete(self):
        self._set_busy(False)
        self.progress_bar.set_fraction(1.0)
        self.progress_bar.set_text("Done")
        self.status_label.set_text("Complete")
        self._show_alert("Download complete", "Download finished successfully")
        self._cancellable = None
        self._download_task = None
        return False

    def _on_download_error(self, message):
        self._set_busy(False)
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_text("0%")
        self.status_label.set_text(f"Error: {message}")
        self._show_alert("Download failed", message)
        self._cancellable = None
        self._download_task = None
        return False

    def _download(self):
        if self._download_task and not self._download_task.get_completed():
            return

        url = self.url_entry.props.text
        format_type = (
            self.format_type_drop_down.props.selected_item.get_string().lower()  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
        )
        quality = (
            self.quality_drop_down.props.selected_item.get_string().strip().lower()  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
        )
        if not self._validate_inputs(url, format_type, quality):
            return
        if self._requires_ffmpeg(format_type, quality) and not self._has_ffmpeg:
            self._show_alert(
                "ffmpeg required", "Install ffmpeg to download video or convert to MP3"
            )
            return
        download_location = self.download_location

        self._set_busy(True)
        self.status_label.set_text("Starting...")
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_text("0%")

        self._cancellable = Gio.Cancellable()
        task = Gio.Task.new(self, self._cancellable, self._download_done, None)

        def _task_func(task, source_object, task_data, cancellable):
            self._download_worker(
                task, cancellable, url, download_location, format_type, quality
            )

        task.run_in_thread(_task_func)
        self.status_label.set_text("Downloading...")
        self._download_task = task

    def _show_alert(self, title, detail):
        Gtk.AlertDialog(
            message=title,
            detail=detail,
            buttons=(["OK"]),
            default_button=0,
            cancel_button=0,
        ).show(self.window)

    def _is_valid_url(self, url):
        parsed = urllib.parse.urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)

    def _validate_inputs(self, url, format_type, quality):
        if not url.strip():
            self._show_alert("Missing URL", "Paste a URL.")
            return False
        if not self._is_valid_url(url):
            self._show_alert("Invalid URL", "Enter a valid http/https URL.")
            return False
        if not format_type:
            self._show_alert("Missing format", "Choose Video or Audio.")
            return False
        if not quality:
            self._show_alert("Missing quality", "Choose a quality/format.")
            return False
        return True

    def _cancel_download(self):
        if self._cancellable and not self._cancellable.is_cancelled():
            self._cancellable.cancel()
            self.status_label.set_text("Cancelling...")

    def _on_download_cancelled(self):
        self._set_busy(False)
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_text("0%")
        self.status_label.set_text("Cancelled")
        self._cancellable = None
        self._download_task = None
        return False

    def _set_quality_options(self, format_type):
        if format_type == "audio":
            options = self._audio_qualities
        else:
            options = self._video_qualities
        quality_list = Gtk.StringList().new(options)
        self.quality_drop_down.set_model(quality_list)
        self.quality_drop_down.set_selected(0)

    def _on_format_type_changed(self, drop_down, _pspec):
        format_type = (
            self.format_type_drop_down.props.selected_item.get_string().lower()  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
        )
        self._set_quality_options(format_type)

    def _requires_ffmpeg(self, format_type, quality):
        return format_type == "video" or quality == "mp3"


def main():
    app = App()
    app.run(None)


if __name__ == "__main__":
    main()
